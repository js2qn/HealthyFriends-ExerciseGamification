from django.forms import ModelForm
from .models import *

# code for the CreateInForum and CreateInDiscussion classes comes from https://data-flair.training/blogs/discussion-forum-python-django/
class CreateInForum(ModelForm):
    class Meta:
        model = ForumPost
        fields = "__all__"

class CreateInDiscussion(ModelForm):
    class Meta:
        model = Discussion
        fields = "__all__"
