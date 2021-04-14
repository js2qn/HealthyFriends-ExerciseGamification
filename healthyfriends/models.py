from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from datetime import date

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


def init_last_seven_days():
    return [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00]
    
class Goals(models.Model): 
    description = models.CharField(max_length=50, default='')
    current_progress = models.DecimalField(max_digits=11, decimal_places=2, default=0.00)
    desired_progress = models.DecimalField(max_digits=11, decimal_places=2, default=1.00)
    metric = models.CharField(max_length=50, default='')
    last_seven_days = ArrayField(models.DecimalField(max_digits=7, decimal_places=2), size=7, default=init_last_seven_days)
    
    last_update = models.DateField(default=date.today)

    QUANTIFIED = 'Y-Metrics'
    TEXTUAL = 'N-Metrics'
    TYPE_OF_GOAL_CHOICES = [
        (QUANTIFIED, 'QUANTIFIED'),
        (TEXTUAL, 'TEXTUAL')
    ]
    goal_type = models.CharField(
        max_length=9,
        choices=TYPE_OF_GOAL_CHOICES,
        default='N-Metrics'
    )

#class Metric(models.Model):
    #goal = models.ForeginKey(Goals, on_delete=models.CASCADE)
    #value = models.DecimalField(max_digits=7, decimal_places=2, default=0.00)





