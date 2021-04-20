from django.db import models
from django.contrib.auth.models import User
from django.db.models import F, Min
from django.db.models.signals import pre_save
import calendar

# Create your models here.
class Workouts(models.Model): 
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField()
    length = models.DecimalField(max_digits=4, decimal_places=1)
    workoutType = models.CharField(max_length=200)
    calories = models.IntegerField()
    points = 1

    def __str__(self):
        #return calendar.month_name[self.date.month]
        return calendar.month_name[self.date.month] + " " + str(self.date.day)

    def __int__(self):
        return self.points


class Profile(models.Model): 
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField() 
    gender = models.CharField(max_length=10)
    weight = models.DecimalField(max_digits=4, decimal_places=1)
    height = models.DecimalField(max_digits=3, decimal_places=1)

class Goals(models.Model):
    name = models.CharField(max_length=200)
    points = models.IntegerField()

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
 
