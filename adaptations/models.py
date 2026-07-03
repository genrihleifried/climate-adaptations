from django.db import models

CLIMATE_IMPACT_CHOICES = [
    ('heat', 'Extreme heat'),
    ('flooding', 'Flooding'),
    ('drought', 'Drought'),
    ('storm', 'Storm'),
    ('wildfire', 'Wildfire'),
    ('water_scarcity', 'Water scarcity'),
    ('extreme_cold', 'Extreme cold'),
    ('ice_and_snow', 'Ice and snow'),
    ('sea_level_rise', 'Sea level rise'),
    ('non_specific', 'Non specific'),
]

TYPE_CHOICES = [
    ('nature_based', 'Nature-based'),
    ('structural', 'Structural / Technical'),
    ('organisational', 'Organisational'),
]

SECTOR_CHOICES = [
    ('urban', 'Urban & infrastructure'),
    ('agriculture', 'Agriculture'),
    ('water', 'Water management'),
    ('health', 'Health'),
    ('energy', 'Energy'),
    ('biodiversity', 'Biodiversity protection'),
    ('forestry', 'Forestry'),
    ('tourism', 'Tourism'),
    ('disaster_risk', 'Disaster risk reduction'),
    ('non_specific', 'Non specific'),
]

class ClimateAdaptation(models.Model):
    name = models.CharField(max_length=200)
    climate_impact = models.CharField(max_length=30, choices=CLIMATE_IMPACT_CHOICES)
    additional_impacts = models.CharField(max_length=200, blank=True)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    sector = models.CharField(max_length=30, choices=SECTOR_CHOICES)

    def __str__(self):
        return self.name