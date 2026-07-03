from django.test import TestCase
from .models import ClimateAdaptation
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

class ClimateAdaptationModelTest(TestCase):
    def test_str_returns_name(self):
        adaptation = ClimateAdaptation.objects.create(
            name="Green roofs",
            climate_impact="heat",
            type="nature_based",
            sector="urban",
        )
        self.assertEqual(str(adaptation), "Green roofs")

class AdaptationFilterTest(TestCase):
    def test_filter_by_climate_impact(self):
        adaptation0 = ClimateAdaptation.objects.create(
            name="Green roofs",
            climate_impact="heat",
            type="nature_based",
            sector="urban",
        )
        adaptation1 = ClimateAdaptation.objects.create(
            name="Adapted crops and varieties",
            climate_impact="drought",
            type="structural",
            sector="agriculture",
        )
        results = ClimateAdaptation.objects.filter(climate_impact="heat")
        self.assertEqual(results.count(), 1)

class CSVUploadTest(TestCase):
    def test_valid_csv_creates_adaptation(self):
        csv_content = (
            "name,climate_impact,type,sector\n"
            "Green roofs,heat,nature_based,urban\n"
        )
        csv_file = SimpleUploadedFile(
            "test.csv",
            csv_content.encode("utf-8"),
            content_type="text/csv",
        )
        self.client.post(reverse("upload_csv"), {"csv_file": csv_file})
        self.assertEqual(ClimateAdaptation.objects.count(), 1)

class InvalidCSVUploadTest(TestCase):
    def test_invalid_csv_is_rejected(self):
        csv_content = (
            "name,climate_impact,type,sector\n"
            "Green roofs,heat,nature_based,tech\n"
        )
        csv_file = SimpleUploadedFile(
            "test.csv",
            csv_content.encode("utf-8"),
            content_type="text/csv",
        )
        self.client.post(reverse("upload_csv"), {"csv_file": csv_file})
        self.assertEqual(ClimateAdaptation.objects.count(), 0)