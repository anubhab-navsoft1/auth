from django.db import models
from datetime import date
# Create your models here
class Category(models.Model):
    title  = models.CharField(max_length = 10, null = False, blank = False)
    description = models.TextField(max_length = 200, null = False)
    
class League(models.Model):
    title = models.CharField(max_length = 10, null = False)
    country = models.CharField(max_length = 10, null = False)
    rank = models.IntegerField(max_length = 10, null = False)

class PlayerDetails(models.Model):
    name = models.CharField(max_length = 255,  null = False)
    date_of_birth = models.DateTimeField()
    team = models.CharField(max_length = 255)
    league = models.ForeignKey(League,on_delete = models.CASCADE, null = False)
    age = models.IntegerField(max_length = 20, null = False)
    
    def save(self, *args, **kwargs):
        self.age = date.today.year - self.date_of_birth.year
        super(PlayerDetails, self).save(*args, **kwargs)

class AchievementDetails(models.Model):
    user = models.ForeignKey(PlayerDetails, on_delete = models.CASCADE, null = False)
    title = models.CharField(max_length = 20,  null = False)
    number = models.IntegerField(max_length = 10, null = False)
    year_won = models.IntegerField(null=True)