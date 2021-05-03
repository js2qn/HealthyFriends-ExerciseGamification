"""mysite URL Configuration


The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from healthyfriends import views 
from django.contrib.auth.decorators import login_required

app_name = 'healthyfriends'
urlpatterns = [
    path('', views.indexView.as_view(), name='index'),
    # path('login/', views.loginView.as_view(), name='login'),
    path('logout', views.logout, name='logout'),
    path('home/', login_required(views.homeView.as_view()), name='home'),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    # path('profile/', login_required(views.profileView.as_view()), name='profile'),
    path('fitnesslog/', login_required(views.fitLog), name='fitnesslog'),
    path('fitnesslog2/', login_required(views.logView2.as_view()), name='fitnesslog2'),
    path('achievements/', login_required(views.achievementsView), name='achievements'),
    path('goals/', login_required(views.goalsView.as_view()), name='goals'),
    path('leaderboard/', login_required(views.leaderboardView), name='leaderboard'),
    # path('forum/', login_required(views.forumView.as_view()), name='forum'),
    # forum, addInForum, and addInDiscussion URLS taken from the following tutorial: https://data-flair.training/blogs/discussion-forum-python-django/ 
    path('forum/', login_required(views.forum), name='forum'),
    path('guides/', login_required(views.guidesView.as_view()), name='guides'),
    path('addInForum/', views.addInForum, name="addInForum"),
    path('addInDiscussion/', views.addInDiscussion, name = 'addInDiscussion'),
    # added for goals by Jayden
    path('updateGoal/', views.updateGoal, name = 'updateGoal'),
    path('addGoal/', views.addGoal, name = 'addGoal'),
    path('deleteGoal/', views.deleteGoal, name='deleteGoal'),
]
