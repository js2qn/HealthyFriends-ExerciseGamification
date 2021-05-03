from django.db.models.functions import RowNumber
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.contrib.auth import logout as auth_logout
from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.views.generic import ListView
from django.contrib.auth import get_user_model
from django.db.models import Sum, Avg, Window
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse
from django import forms
from django.db.models import F

from quickchart import QuickChart

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
            pts, _ = Points.objects.get_or_create(user = request.user)
            pts.points = F('points') + 1
            pts.save()
            #pts = Points(user = request.user, points =1)
            #pts = Points.objects.filter(user = request.user).update(points = F('points')+1)
            workout.save()
        newqc = createChart(request.user)
        newqc_url = (newqc.get_url)
        return render(request, 'healthyfriends/fitnesslog.html', {'quickchart_url': newqc_url})
    else:
        qc = createChart(request.user)
        qc_url = (qc.get_url)
        return render(request, 'healthyfriends/fitnesslog.html', {'quickchart_url': qc_url})
        

class logView2(TemplateView): 
    template_name = 'healthyfriends/fitnesslog2.html'

#def updatePoints(request):
#    if request.method == 'POST':
#        pts = Points()
#        pts.user = request.user
#        pts.points += 1
#    return render(request, 'healthyfriends/fitnesslog.html')

def achievementsView(request):
    #pts = Points.objects.filter(user=request.user).count()
    #achievements_ct = Points.objects.filter(user=request.user)
    achievements_ct = Points.objects.get(user=request.user).points
    achievements = Workouts.objects.filter(user=request.user).order_by('-date')
    return render(request, 'healthyfriends/achievements.html', {'achievements_ct':achievements_ct, 'achievements':achievements})

def leaderboardView(request):
    rank = 1
    ranking = [] #
    this_user = get_user_model()
    us = this_user.objects.all()
    egg = Points.objects.all()

    users = Points.objects.order_by('-points') #

    user_list = list(us)

    point_users = list(users)
    more_users = []
    pts = []

    for i in users:
        i = str(i)
        pts.append(i.split()[1])
        more_users.append(i.split()[0])

    #for i in users:
    #    pt = i.points
     #   pts.append(pt)

    user_ct = this_user.objects.count()

    for i,x  in enumerate(us[0:]):
        ranking.append(rank)
        rank = rank + 1
        x.rank = rank
        if(rank > Points.objects.count()):
            break;

    #for i in user_list:
    #    if(i not in point_users):
    #        more_users.append(None)

    #while(len(pts) < user_ct):
    #    pts.append(0)

    return render(request, 'healthyfriends/leaderboard.html', {'user_ct':user_ct, 'users':more_users, 'rank':ranking, 'pts':pts})
#class achievementsView(TemplateView):
#    template_name = 'healthyfriends/achievements.html'

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
            pts, _ = Points.objects.get_or_create(user = request.user)
            pts.points = F('points') + 5
            pts.save()
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

#class leaderboardView(TemplateView):
   # template_name = 'healthyfriends/leaderboard.html'

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
            # if valid form, don't save the model just yet
            # instead, first get the logged user's username and set the forum post's name to that
            usernameless = form.save()
            usernameless.name = request.user.get_username()
            usernameless.save()

            return redirect('forum')
    context = {'form':form}
    return render(request, 'healthyfriends/addInForum.html', context)

def addInDiscussion(request):
    form = CreateInDiscussion()
    if request.method=='POST':
        form = CreateInDiscussion(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.name = request.user.get_username()
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
      
    
def createChart(user) :
    qc = QuickChart()
    qc.width = 500
    qc.height = 300
    qc.device_pixel_ratio = 2.0
    user_workouts_list = []
    objects = Workouts.objects.order_by('-date')
    for workout in objects:
        if user == workout.user:
            user_workouts_list.append(workout)
    latest_workouts_list = user_workouts_list[:50]
    calories_list = []
    date_list = []
    for w in reversed(latest_workouts_list):
        date_list.append(w.date.strftime("%m-%d-%Y"))
        calories_list.append(w.calories)
    qc.config = {
        "type": "line",
        "data": {
            "labels": date_list,
            "datasets": [{
                "label": "Calories burned",
                "data": calories_list
            }]
        }
    }
    return qc
