from django.db import models

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
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    cows_count = models.IntegerField(default=0)  # Number of cows
    bulls_count = models.IntegerField(default=0)  # Number of bulls

    @property
    def total_cattle(self):
        return self.cows_count + self.bulls_count
