from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Workouts(models.Model): 
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField()
    length = models.DecimalField(max_digits=4, decimal_places=1)
    workoutType = models.CharField(max_length=200)
    calories = models.IntegerField()

class Profile(models.Model): 
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField() 
    gender = models.CharField(max_length=10)
    weight = models.DecimalField(max_digits=4, decimal_places=1)
    height = models.DecimalField(max_digits=3, decimal_places=1)

class Goals(models.Model): 
    name = models.CharField(max_length=200) 
    points = models.IntegerField()

