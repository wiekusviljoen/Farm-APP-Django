from django.db import models
from datetime import datetime, timedelta


Breed_CATEGORY =(
    ('Bonsmara', 'Bonsmara'),
    ('Brahman', 'Brahman'),
    ('Jersey', 'Jersey'),
    ('Muliple','Multiple')
)

Vaccine_CATEGORY = (
    ('Multivax', 'Multivax'),
    ('Disulfox', 'Disulfox'),
    ('Terramycin', 'Terramycin'),
    ('None','None')
)   

Feed_CATEGORY = (
    ('Energie Lek','Energie Lek'),
    ('Beef Finisher', 'Beef Finisher'),
    ('Koei & Kalf', 'Koei & Kalf'),
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
    breed = models.CharField(max_length=100,choices=Breed_CATEGORY,null = True)
    cows_count = models.IntegerField(default=0)  # Number of cows
    bulls_count = models.IntegerField(default=0)  # Number of bulls
    calf_count = models.IntegerField(default=0)
    vaccine1 = models.CharField(max_length=100,choices=Vaccine_CATEGORY,null = True)
    vaccine2 = models.CharField(max_length=100,choices=Vaccine_CATEGORY,null = True)
    vaccine3 = models.CharField(max_length=100,choices=Vaccine_CATEGORY,null = True)
    is_branded = models.BooleanField(default=False)
    pregnant_cows = models.IntegerField(default=0)
    sick = models.IntegerField(default=0)
    Feed = models.CharField(max_length=100,choices=Feed_CATEGORY,null = True)
    feed_cost = models.FloatField( default=0)
    notes = models.CharField(max_length=100 , null=True)


    def total_feed_cost(self):
        days_registered = self.days_since_registration
        if days_registered is not None:
            feed_cost_per_day = self.feed_cost_per_day()
            total_cost = feed_cost_per_day * days_registered
            rounded_cost = round(total_cost, 2)  # Round the total cost to 2 decimal places
            return rounded_cost
        else:
            return None


    @property
    def total_cattle(self):
        return self.cows_count + self.bulls_count + self.calf_count
    
    
        
    def feed_cost_per_day(self):
    # Adjusting the feed per cow per day value
        feed_per_cow_per_day = 2  # You can adjust this value based on your requirements

    # Calculating total feed required per day for all cattle
        total_feed_per_day = (self.cows_count * feed_per_cow_per_day) + (self.bulls_count * feed_per_cow_per_day * 1.5) + (self.calf_count * feed_per_cow_per_day * 0.5)

    # Calculating total feed cost per day based on the price per bag and total cattle weight
        feed_cost_per_day = total_feed_per_day * (self.feed_cost / 50)

        return feed_cost_per_day



 

    @property
    def days_since_registration(self):
        if self.date:
            # Calculate the difference between the current date and the registration date
            difference = datetime.now().date() - self.date
            return difference.days
        else:
            return None 

   


