from django.db import models

from django.db import models

KLIMAFOLGE_CHOICES = [
    ('hitze', 'Hitze'),
    ('hochwasser', 'Hochwasser'),
    ('duerre', 'Dürre'),
    ('sturm', 'Sturm'),
    ('waldbrand', 'Waldbrand'),
]

TYP_CHOICES = [
    ('naturbasiert', 'Naturbasiert'),
    ('baulich', 'Baulich-technisch'),
    ('organisatorisch', 'Organisatorisch'),
]

SEKTOR_CHOICES = [
    ('stadt', 'Stadt & Infrastruktur'),
    ('landwirtschaft', 'Landwirtschaft'),
    ('wasser', 'Wasser'),
    ('gesundheit', 'Gesundheit'),
    ('energie', 'Energie'),
]

KOSTEN_CHOICES = [
    ('niedrig', 'Niedrig'),
    ('mittel', 'Mittel'),
    ('hoch', 'Hoch'),
]

class ClimateAdaptations(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    klimafolge = models.CharField(max_length=20, choices=KLIMAFOLGE_CHOICES)
    typ = models.CharField(max_length=20, choices=TYP_CHOICES)
    sektor = models.CharField(max_length=20, choices=SEKTOR_CHOICES)
    region = models.CharField(max_length=200, blank=True)
    kosten = models.CharField(max_length=10, choices=KOSTEN_CHOICES)
    quelle = models.URLField(blank=True)

    def __str__(self):
        return self.name
