from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.contrib.auth import logout as auth_logout
from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django import forms

from .models import Workouts, User

# Create your views here.


def logout(request):
    auth_logout(request)
    return redirect('index')

class loginView(TemplateView): 
    template_name = 'healthyfriends/login.html'

class indexView(TemplateView): 
    template_name = 'healthyfriends/index.html'

class homeView(TemplateView): 
    template_name = 'healthyfriends/home.html'

def checkLogin(request): 
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('home'))
    else: 
        return redirect('login')

class logView(TemplateView): 
    template_name = 'healthyfriends/fitnesslog.html'

def fitLog(request):
    if request.method == 'POST':
        if request.POST.get('date') and request.POST.get('length') and request.POST.get('activity'):
            workout = Workouts()
            workout.user = request.user
            workout.date = request.POST.get('date')
            workout.length = request.POST.get('length')
            workout.workoutType = request.POST.get('activity')
            workout.calories = request.POST.get('calories')
            workout.save()
        return render(request, 'healthyfriends/fitnesslog.html', None)
    else:
        return render(request, 'healthyfriends/fitnesslog.html', None)

class logView2(TemplateView): 
    template_name = 'healthyfriends/fitnesslog2.html'

class achievementsView(TemplateView): 
    template_name = 'healthyfriends/achievements.html'

class profileView(TemplateView): 
    template_name = 'healthyfriends/profile.html'

class leaderboardView(TemplateView): 
    template_name = 'healthyfriends/leaderboard.html'

class forumView(TemplateView): 
    template_name = 'healthyfriends/forum.html'

class guidesView(TemplateView): 
    template_name = 'healthyfriends/guides.html'