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
from django.db.models import F
from .models import *
from .forms import *
from decimal import Decimal
# Create your views here.


def logout(request):
    auth_logout(request)
    return redirect('index')

# class loginView(TemplateView): 
#     template_name = 'healthyfriends/login.html'

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
###################################################################################
###################################################################################

class goalsView(ListView): 
    template_name = 'healthyfriends/goals.html'
    context_object_name = 'goals_list'

    def get_queryset(self):
        return Goals.objects.all().order_by('-last_update', 'description')

    def get_context_data(self, **kwargs):
        context = super(goalsView, self).get_context_data(**kwargs)
        context['goalsInProgress'] = Goals.objects.filter(desired_progress__gt=F('current_progress')).order_by('-last_update', 'description')
        context['goalsCompleted'] = Goals.objects.filter(desired_progress__lte=F('current_progress')).order_by('-last_update', 'description')
        #context['myGoals'] = Goals.objects.filter(goal_belongs_to)
        return context

def updateGoal(request):
    goal_id = request.POST.get("id")
    goal_user = request.POST.get("username")

    mt = "metrics-toggle-" + goal_id
    descrp = "description-" + goal_id
    cur = "current-" + goal_id
    goal = get_object_or_404(Goals, pk=goal_id)
    
    if (request.POST.get("descrp") == ''):
        return render(request, 'healthyfriends/goals.html', {
            'error_message': "Please Add A Description."
        })

    if (request.POST.get(mt) == "Y-Metrics"):
        des = "desired-" + goal_id
        met = "metric-" + goal_id
        
        if (request.POST.get(cur) == '' or request.POST.get(des) == ''):
            return render(request, 'healthyfriends/goals.html', {
                'goalsInProgress': Goals.objects.filter(desired_progress__gt=F('current_progress')).order_by('-last_update'),
                'goalsCompleted': Goals.objects.filter(desired_progress__lte=F('current_progress')).order_by('-last_update'),
                'error_message': "Please fill both progess fields to update."
            })
        goal.goal_belongs_to = goal_user
        goal.description = request.POST.get(descrp)
        goal.current_progress = round(Decimal(request.POST.get(cur)), 2)
        goal.desired_progress = round(Decimal(request.POST.get(des)), 2)
        goal.metric = request.POST.get(met)
        goal.goal_type = "Y-Metrics"
        goal.last_update = date.today()

    elif(request.POST.get(mt) == "N-Metrics"):
        goal.description = request.POST.get(descrp)
        
        if(round(Decimal(request.POST.get(cur)), 2) >= 1):
            goal.current_progress = 1.00
        elif (round(Decimal(request.POST.get(cur)), 2) >= 0 and round(Decimal(request.POST.get(cur)), 2) < 1):
            goal.current_progress = 0.00
         
        goal.desired_progress = 1.00
        goal.metric = ""
        goal.goal_type = "N-Metrics"
        goal.last_update = date.today()

    goal.save()
    return HttpResponseRedirect(reverse('goals'))  # changed for merge purposes


def addGoal(request):

    goal_user = request.POST.get("username")

    descrp = request.POST.get("description-add")
    mt = request.POST.get("metrics-toggle-add")
    cur = request.POST.get("current-add")

    if (mt == "Y-Metrics"):
        des = request.POST.get("desired-add")
        met = request.POST.get("metric-add")

        if (descrp == "" or met == "" or cur == "" or des == ""):
            return render(request, 'healthyfriends/goals.html', {
                'goalsInProgress': Goals.objects.filter(desired_progress__gt=F('current_progress')).order_by('-last_update'),
                'goalsCompleted': Goals.objects.filter(desired_progress__lte=F('current_progress')).order_by('-last_update'),
                'error_message': "Please fill all available fields to add goal.",
        })
        else:
            cur_decimal = round(Decimal(cur), 2)
            des_decimal = round(Decimal(des), 2)
            goal = Goals.objects.create(goal_belongs_to=goal_user, description=descrp, current_progress=cur_decimal, desired_progress=des_decimal, metric=met, goal_type="Y-Metrics")
            return HttpResponseRedirect(reverse('goals'))

    if (mt == "N-Metrics"):
        if (descrp == "" or cur == ""):
            return render(request, 'healthyfriends/goals.html', {
                'goalsInProgress': Goals.objects.filter(desired_progress__gt=F('current_progress')).order_by('-last_update'),
                'goalsCompleted': Goals.objects.filter(desired_progress__lte=F('current_progress')).order_by('-last_update'),
                'error_message': "Please fill all available fields to add goal.",
        })
        else:
            cur_decimal = round(Decimal(cur), 2)
            goal = Goals.objects.create(goal_belongs_to=goal_user, description=descrp, current_progress=cur_decimal, goal_type="N-Metrics")
            return HttpResponseRedirect(reverse('goals'))


def deleteGoal(request):
    idToDel = int(request.POST.get("id"))
    Goals.objects.filter(id=idToDel).delete()

    return HttpResponseRedirect(reverse('goals'))


###################################################################################
###################################################################################
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