from django.forms import ModelForm
from .models import *

# code for the CreateInForum and CreateInDiscussion classes comes from https://data-flair.training/blogs/discussion-forum-python-django/
class CreateInForum(ModelForm):
    class Meta:
        model = ForumPost
        fields = ('topic', 'description')

class CreateInDiscussion(ModelForm):
    class Meta:
        model = Discussion
        fields = ('forum', 'discuss')
