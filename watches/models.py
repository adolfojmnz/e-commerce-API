from django.db import models


MOVEMENT_OPTIONS = [
    ('Q', 'QUARTZ'),
    ('A', 'AUTOMATIC'),
    ('S', 'SOLAR'),
]

CASE_MATERIAL_OPTIONS = [
    ('M-W', 'METAL-WOOD'),
    ('W', 'WOOD'),
    ('M', 'METAL'),
]

BRACELET_MATERIAL_OPTIONS = [
    ('M-W', 'METAL-WOOD'),
    ('S-M', 'STONE-METAL'),
    ('M', 'METAL'),
    ('W', 'WOOD'),
    ('L', 'LETHER'),
]

COLOR_OPTIONS = [
    ('D', 'DARK'),
    ('L', 'LIGHT'),
    ('F', 'COLOURFUL'),
]


class Watch(models.Model):
    collection = models.ForeignKey(
        'watches.Collection', on_delete=models.PROTECT, related_name='watches',
    )
    model_name = models.CharField(max_length=128)
    is_waterproof = models.BooleanField(default=False)
    has_date_indicator = models.BooleanField(default=False)
    has_cronograph_features = models.BooleanField(default=False)
    color = models.CharField(choices=COLOR_OPTIONS, max_length=1)
    diameter = models.IntegerField(help_text="Watch diameter in mm")
    movement = models.CharField(choices=MOVEMENT_OPTIONS, max_length=1)
    case_material = models.CharField(choices=CASE_MATERIAL_OPTIONS, max_length=3)
    bracelet_material = models.CharField(choices=BRACELET_MATERIAL_OPTIONS, max_length=3)
    release_date = models.DateField()
    description = models.CharField(max_length=512)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = ['collection', 'model_name']

    def __str__(self) -> str:
        return self.model_name


class Collection(models.Model):
    vendor = models.ForeignKey('accounts.User', on_delete=models.PROTECT)
    name = models.CharField(max_length=128)
    brand = models.CharField(max_length=128)
    description = models.CharField(max_length=256)
    release_date = models.DateField()

    class Meta:
        unique_together = ['name', 'brand']

    def __str__(self) -> str:
        return self.name
