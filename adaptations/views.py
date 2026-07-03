import csv
import io

from django.contrib import messages
from django.shortcuts import render, redirect

from .forms import CSVUploadForm
from .models import (
    ClimateAdaptation,
    CLIMATE_IMPACT_CHOICES,
    TYPE_CHOICES,
    SECTOR_CHOICES,
)


def adaptation_list(request):
    adaptations = ClimateAdaptation.objects.all()

    climate_impact = request.GET.get("climate_impact", "")
    type_ = request.GET.get("type", "")
    sector = request.GET.get("sector", "")

    if climate_impact:
        adaptations = adaptations.filter(climate_impact=climate_impact)
    if type_:
        adaptations = adaptations.filter(type=type_)
    if sector:
        adaptations = adaptations.filter(sector=sector)

    context = {
        "adaptations": adaptations,
        "climate_impact_choices": CLIMATE_IMPACT_CHOICES,
        "type_choices": TYPE_CHOICES,
        "sector_choices": SECTOR_CHOICES,
        "selected_climate_impact": climate_impact,
        "selected_type": type_,
        "selected_sector": sector,
    }

    return render(request, "adaptations/adaptation_list.html", context)


def upload_csv(request):
    if request.method == "POST":
        form = CSVUploadForm(request.POST, request.FILES)

        if form.is_valid():
            csv_file = request.FILES["csv_file"]

            # Ensure the uploaded file is a CSV
            if not csv_file.name.lower().endswith(".csv"):
                messages.error(
                    request,
                    "Please upload a file with a .csv extension."
                )
                return redirect("upload_csv")

            # Decode the uploaded file
            try:
                decoded_file = csv_file.read().decode("utf-8")
            except UnicodeDecodeError:
                messages.error(
                    request,
                    "File could not be read (please use UTF-8 encoding)."
                )
                return redirect("upload_csv")

            reader = csv.DictReader(io.StringIO(decoded_file))

            # Check required columns
            required_fields = {"name", "climate_impact", "type", "sector"}
            available_fields = set(reader.fieldnames or [])

            if not required_fields.issubset(available_fields):
                missing = required_fields - available_fields
                messages.error(
                    request,
                    f"Missing columns: {', '.join(sorted(missing))}"
                )
                return redirect("upload_csv")

            valid_impact = dict(CLIMATE_IMPACT_CHOICES)
            valid_type = dict(TYPE_CHOICES)
            valid_sector = dict(SECTOR_CHOICES)

            created_count = 0
            errors = []

            for row_number, row in enumerate(reader, start=2):
                name = (row.get("name") or "").strip()
                climate_impact = (row.get("climate_impact") or "").strip()
                type_ = (row.get("type") or "").strip()
                sector = (row.get("sector") or "").strip()

                # Validate required values
                if not name:
                    errors.append(f"Row {row_number}: 'name' is missing.")
                    continue

                if climate_impact not in valid_impact:
                    errors.append(
                        f"Row {row_number}: invalid climate_impact '{climate_impact}'."
                    )
                    continue

                if type_ not in valid_type:
                    errors.append(
                        f"Row {row_number}: invalid type '{type_}'."
                    )
                    continue

                if sector not in valid_sector:
                    errors.append(
                        f"Row {row_number}: invalid sector '{sector}'."
                    )
                    continue

                ClimateAdaptation.objects.create(
                    name=name,
                    climate_impact=climate_impact,
                    type=type_,
                    sector=sector,
                )

                created_count += 1

            if created_count:
                messages.success(
                    request,
                    f"Successfully imported {created_count} adaptation(s)."
                )

            for error in errors:
                messages.error(request, error)

            return redirect("adaptation_list")

    else:
        form = CSVUploadForm()

    return render(
        request,
        "adaptations/upload_csv.html",
        {"form": form},
    )
