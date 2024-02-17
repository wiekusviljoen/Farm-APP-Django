from django.db import models
from datetime import datetime, timedelta


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
    pregnant_cows = models.IntegerField(default=0)
    feed_cost = models.IntegerField(default=0)

    @property
    def total_cattle(self):
        return self.cows_count + self.bulls_count + self.calf_count
    
    def feed(self):
        return self.cows_count * 13
        
    def feed_cost_per_day(self):
        feed_per_cow_per_day = 13 # Adjust this value according to your requirements
        total_feed_per_day = self.cows_count * feed_per_cow_per_day
        feed_cost_per_day = total_feed_per_day * self.feed_cost / 50
        return feed_cost_per_day  

    @property
    def days_since_registration(self):
        if self.date:
            # Calculate the difference between the current date and the registration date
            difference = datetime.now().date() - self.date
            return difference.days
        else:
            return None 

    @property
    def percentage_pregnant_cows(self):
        if self.cows_count > 0:
            return round((self.pregnant_cows / self.cows_count) * 100)
        else:
            return 0


