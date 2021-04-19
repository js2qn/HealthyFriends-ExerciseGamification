from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.contrib.auth import logout as auth_logout
from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse
from django import forms
from django.urls import reverse

from .models import *
from .forms import *

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

class achievementsView(ListView): 
    template_name = 'healthyfriends/achievements.html'
    context_object_name = 'goals_list'

    def get_queryset(self):
        return Goals.objects.all()

def update_Goal(request):
    goal_id = request.POST.get("id")
    goal = get_object_or_404(Goals, pk=goal_id)

    if(request.POST.get("metrics-toggle-" + goal_id) == "Y-Metrics"):
        goal.description = request.POST.get("description-" + goal_id)
        goal.current_progress = request.POST.get("current-" + goal_id)
        goal.desired_progress = request.POST.get("desired-" + goal_id)
        goal.metric = request.POST.get("metric-" + goal_id)
        goal.goal_type = "Y-Metrics"
        goal.last_update = date.today()
    elif(request.POST.get("metrics-toggle-" + goal_id) == "N-Metrics")
        goal.description = request.POST.get("description-" + goal_id)
        goal.current_progress = 0.00
        goal.desired_progress = 1.00
        goal.metric = ""
        goal.goal_type = "N-Metrics"
        goal.last_update = date.today()

    goal.save()
    return # this is where I stopped
class profileView(TemplateView): 
    template_name = 'healthyfriends/profile.html'

class leaderboardView(TemplateView): 
    template_name = 'healthyfriends/leaderboard.html'
"""
class forumView(TemplateView): 
    template_name = 'healthyfriends/forum.html'
    forums=ForumPost.objects.all()
    count = forums.count()
    discussions=[]
    for discussion in forums:
        discussions.append(discussion.discussion.set_all())
"""
# following tutorial for the forum views (forum, addInForum, addInDiscussion), defined down here
# tutorial located at https://data-flair.training/blogs/discussion-forum-python-django/ 
def forum(request):
    forums = ForumPost.objects.all()
    count = forums.count()
    discussions = []
    for discussion in forums:
        discussions.append(discussion.discussion_set.all())
    
    context={
        'forums':forums,
        'count':count,
        'discussions':discussions
    }
    print(discussions)
    return render(request, 'healthyfriends/forum.html', context)

def addInForum(request):
    form = CreateInForum()
    if request.method=='POST':
        form = CreateInForum(request.POST)
        if form.is_valid():
            form.save()
            return redirect('forum')
    context = {'form':form}
    return render(request, 'healthyfriends/addInForum.html', context)

def addInDiscussion(request):
    form = CreateInDiscussion()
    if request.method=='POST':
        form = CreateInDiscussion(request.POST)
        if form.is_valid():
            form.save()
            return redirect('forum')
    context={'form':form}
    return render(request, 'healthyfriends/addInDiscussion.html', context)
# end not our IP
class guidesView(ListView): 
    template_name = 'healthyfriends/guides.html'
    context_object_name = 'videos_list'

    def get_queryset(self):
        return Videos.objects.all()




"""
    <div class="progress">
        <div class="progress-bar progress-bar-striped progress-bar-animated" role="progressbar" style="width:{{ goal.current_progress }}|intdiv:{{ goal.desired_progress }}%" aria-valuenow="{{ goal.current_progress }}|intdiv:{{ goal.desired_progress }}" aria-valuemin="0" aria-valuemax="100">
        </div>
      </div>


    <div class="tab-pane" id="history" role="tabpanel" aria-labelledby="history-tab">  
    <p class="card-text">First settled around 1000 BCE and then founded as the Etruscan Felsina about 500 BCE, it was occupied by the Boii in the 4th century BCE and became a Roman colony and municipium with the name of Bononia in 196 BCE. </p>
    <a href="#" class="card-link text-danger">Read more</a>
    </div>
"""  