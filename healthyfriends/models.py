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
    metric = models.CharField(max_length=50, default="")
    last_seven_days = ArrayField(models.DecimalField(max_digits=7, decimal_places=2), size=7, default=init_last_seven_days)

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

    last_update = models.DateField(default=date.today)

    def __str__(self):
        return self.description

#class Metric(models.Model):
    #goal = models.ForeginKey(Goals, on_delete=models.CASCADE)
    #value = models.DecimalField(max_digits=7, decimal_places=2, default=0.00)





class Videos(models.Model):
    # this isn't really all that special, just allows us to easily add videos from admin page instead of having to update the HTML and repush
    # this is the embed stuff you get from the YouTube share option 
    embed = models.CharField(max_length=300)
    # this holds a short description about the content of each video
    description = models.CharField(max_length=200)

# the basic code structuring the forum comes from the following source: https://data-flair.training/blogs/discussion-forum-python-django/ 
# This includes the ForumPost and Discussion models
# TODO: Associate forum posts and discussions with our users instead of having 0 association
class ForumPost(models.Model):
    """
    ForumPost consists of a name, topic, description, link, and date created
    """
    name = models.CharField(max_length=200, default="anonymous")
    topic = models.CharField(max_length=300)
    description = models.CharField(max_length=1000, blank=True)
    link = models.CharField(max_length=100, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    
    """
    ForumPost string rep is of the post's topic
    """
    def __str__(self):
        return str(self.topic)

class Discussion(models.Model):
    forum = models.ForeignKey(ForumPost, blank=True, on_delete=models.CASCADE)
    discuss = models.CharField(max_length=1000)
    """
    Discussion string rep is of the post's topic
    """
    def __str__(self):
        return str(self.discuss)
 
