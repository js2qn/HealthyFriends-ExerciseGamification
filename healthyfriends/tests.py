from django.test import TestCase
from django.urls import reverse, reverse_lazy
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

from .models import Videos
# Create your tests here.
# Creating dummy code

def createVideo(embedURL, description):
    """
    Create a video object with the given embedURL and description
    """
    return Videos.objects.create(embed=embedURL, description=description)

def testLogin(user,email, password):
    user = User.objects.create_user(user, email, password)
    return user

class DummyTest(TestCase):
    def test_dummy(self):
        self.assertIs(True, True)

# Testing for the guides view
class GuidesViewTest(TestCase):
    def test_no_videos(self):
        """
        Testing the no_videos case
        """
        # this line forces the client to login, allows us to access the url via reverse
        # idea comes from https://stackoverflow.com/questions/2619102/djangos-self-client-login-does-not-work-in-unit-tests user Muthuvel
        self.client.force_login(User.objects.get_or_create(username='testuser')[0])
        response = self.client.get(reverse('guides'))
        self.assertIs(response.status_code, 200)
        self.assertQuerysetEqual(response.context['videos_list'],[])
    
    def test_one_video(self):
        """
        Testing the one video case
        """
        createVideo("https://www.youtube.com/embed/ljG1WzBAboQ", "helpful")
        self.client.force_login(User.objects.get_or_create(username='testuser')[0])
        response = self.client.get(reverse('guides'))
        self.assertIs(response.status_code, 200)
        self.assertQuerysetEqual(list(response.context['videos_list']), ['<Videos: Videos object (1)>'])
    def test_mult_video(self):
        """
        Testing the multi-video case
        """
        createVideo("https://www.youtube.com/embed/ljG1WzBAboQ", "helpful1")
        createVideo("https://www.youtube.com/embed/ljG1WzBAboQ", "helpful2")
        self.client.force_login(User.objects.get_or_create(username='testuser')[0])
        response = self.client.get(reverse('guides'))
        self.assertIs(response.status_code, 200)
        self.assertQuerysetEqual(list(response.context['videos_list']), ['<Videos: Videos object (1)>', '<Videos: Videos object (2)>'])