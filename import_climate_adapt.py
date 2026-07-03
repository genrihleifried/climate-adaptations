"""
Automation tool: downloads climate adaptation options from the EU Climate-ADAPT
platform, maps them to this app's data structure and writes a normalised CSV
that can be imported via the app's CSV upload.
"""

import csv
import io
import json
import sys

import requests



DOWNLOAD_URL = "https://climate-adapt.eea.europa.eu/_es/ccaSearch/_download"

QUERY = {
    "searchTerm": "",
    "filters": [
        {"field": "language", "type": "any", "values": ["en"]},
        {"field": "objectProvides", "type": "any", "values": ["Adaptation option"]},
    ],
}

OUTPUT_FILE = "adaptations_import.csv"


CLIMATE_IMPACT_MAP = {
    "Extreme heat": "heat",
    "Flooding": "flooding",
    "Droughts": "drought",
    "Storms": "storm",
    "Wildfires": "wildfire",
    "Water Scarcity": "water_scarcity",
    "Extreme cold": "extreme_cold",
    "Ice and Snow": "ice_and_snow",
    "Sea Level Rise": "sea_level_rise",
    "Non specific": "non_specific",
}

TYPE_MAP = {
    "Nature-based solutions": "nature_based",
    "Adaptation Measures and Actions": "structural",
    "Sector Policies": "organisational",
    "Adaptation Plans and Strategies": "organisational",
    "Climate services": "organisational",
}

SECTOR_MAP = {
    "Health": "health",
    "Agriculture": "agriculture",
    "Water management": "water",
    "Energy": "energy",
    "Biodiversity protection": "biodiversity",
    "Forestry": "forestry",
    "Tourism": "tourism",
    "Disaster Risk Reduction": "disaster_risk",
    "Non specific": "non_specific",
}

CODE_TO_NAME = {
    "heat": "Extreme heat",
    "flooding": "Flooding",
    "drought": "Drought",
    "storm": "Storm",
    "wildfire": "Wildfire",
    "water_scarcity": "Water scarcity",
    "extreme_cold": "Extreme cold",
    "ice_and_snow": "Ice and snow",
    "sea_level_rise": "Sea level rise",
    "non_specific": "Non specific",
}

# Uses the platform's CSV download endpoint (POST)
def download_csv():
    form_data = {"query": json.dumps(QUERY)}

    try:
        response = requests.post(DOWNLOAD_URL, data=form_data, timeout=30)
        response.raise_for_status()
    except requests.RequestException as error:
        print(f"Error: {error}")
        sys.exit(1)

    return response.text


def split_values(raw):
    if not raw:
        return []
    return [v.strip() for v in raw.split(",") if v.strip()]

# A single adaptation can address several climate impacts. The data model keeps
# one filterable value, so the first mapped impact becomes the primary field
def map_climate_impact(raw):
    codes = []

    for value in split_values(raw):
        code = CLIMATE_IMPACT_MAP.get(value)
        if code and code not in codes:
            codes.append(code)

    if not codes:
        return None, ""

    primary = codes[0]
    additional = ", ".join(CODE_TO_NAME[c] for c in codes[1:])

    return primary, additional


def map_first(raw, mapping):
    for value in split_values(raw):
        code = mapping.get(value)
        if code:
            return code
    return None
# Skip rows whose required category cannot be mapped
def process(csv_text):
    reader = csv.DictReader(io.StringIO(csv_text))

    output_rows = []
    skipped = 0

    for row in reader:
        name = (row.get("Title") or "").strip()

        if not name:
            skipped += 1
            continue

        climate_impact, additional_impacts = map_climate_impact(
            row.get("Climate impact", "")
        )

        sector = map_first(row.get("Sectors", ""), SECTOR_MAP)
        adaptation_type = map_first(
            row.get("Adaptation Approaches", ""),
            TYPE_MAP,
        )

        if not climate_impact or not sector or not adaptation_type:
            skipped += 1
            continue

        output_rows.append({
            "name": name,
            "climate_impact": climate_impact,
            "additional_impacts": additional_impacts,
            "type": adaptation_type,
            "sector": sector,
        })

    return output_rows, skipped

def write_csv(rows):
    fieldnames = [
        "name",
        "climate_impact",
        "additional_impacts",
        "type",
        "sector",
    ]

    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

def main():

    csv_text = download_csv()

    

    rows, skipped = process(csv_text)

    write_csv(rows)

    print(f"{len(rows)} Entry saved.")
    print(f"{skipped} Entry skipped.")
    print(f"CSV saved as'{OUTPUT_FILE}'.")


if __name__ == "__main__":
    main()