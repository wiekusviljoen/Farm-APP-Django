from django.db import models


CATEGORY =(
    ('Bonsmara', 'Bonsmara'),
    ('Brahman', 'Brahman'),
    ('Jersey', 'Jersey'),
    ('Muliple','Multiple')
)

CATEGORY2 = (
    ('Multivax', 'Multivax'),
    ('Disulfox', 'Disulfox'),
    ('Terramycin', 'Terramycin'),
    ('None','None')
)   

class Cow(models.Model):
    name = models.CharField(max_length=100)
    breed = models.CharField(max_length=100)
    age = models.IntegerField()
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    is_pregnant = models.BooleanField(default=False)

class Bull(models.Model):
    name = models.CharField(max_length=100)
    breed = models.CharField(max_length=100)
    age = models.IntegerField()
    weight = models.DecimalField(max_digits=5, decimal_places=2)

class Farm(models.Model):
    date = models.DateField(null=True)
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    breed = models.CharField(max_length=100,choices=CATEGORY,null = True)
    cows_count = models.IntegerField(default=0)  # Number of cows
    bulls_count = models.IntegerField(default=0)  # Number of bulls
    calf_count = models.IntegerField(default=0)
    vaccine1 = models.CharField(max_length=100,choices=CATEGORY2,null = True)
    vaccine2 = models.CharField(max_length=100,choices=CATEGORY2,null = True)
    vaccine3 = models.CharField(max_length=100,choices=CATEGORY2,null = True)
    is_branded = models.BooleanField(default=False)

    @property
    def total_cattle(self):
        return self.cows_count + self.bulls_count + self.calf_count

