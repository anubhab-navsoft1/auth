from django.db import models
from datetime import date
from django.core.exceptions import ValidationError
# Create your models here
class Category(models.Model):
    title  = models.CharField(max_length = 10, null = False, blank = False)
    description = models.TextField(max_length = 200, null = False)
    
class League(models.Model):
    related_sport = models.ForeignKey(Category, on_delete = models.CASCADE, null = False, default = None)
    title = models.CharField(max_length = 10, null = False)
    country = models.CharField(max_length = 10, null = False)
    rank = models.IntegerField(max_length = 10, null = False)

class PlayerDetails(models.Model):
    name = models.CharField(max_length=255, null=False)
    date_of_birth = models.DateField()
    team = models.CharField(max_length=255)
    league = models.ForeignKey(League, on_delete=models.CASCADE, null=False)

    def calculate_age(self):
        today = date.today()
        age = today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
        return age

    def clean(self):
        if self.date_of_birth > date.today():
            raise ValidationError("Date of birth cannot be in the future.")

    def __str__(self):
        return self.league.title
        
class AchievementDetails(models.Model):
    player = models.ForeignKey(PlayerDetails, on_delete = models.CASCADE, null = False)
    title = models.CharField(max_length = 20,  null = False)
    number = models.IntegerField(max_length = 10, null = False)
    year_won = models.IntegerField(null=True)
    
    def __str__(self) -> str:
        return self.player.name