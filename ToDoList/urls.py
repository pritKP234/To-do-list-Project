"""
URL configuration for ToDoList project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path,re_path
from app.views import *
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/',CustomLoginView.as_view(),name='login'),
    path('logout/',LogoutView.as_view(next_page='login'),name='logout'),
    path('register/',RegisterPage.as_view(),name='register'),
    path('admin/', admin.site.urls),
    path('TaskList/',TaskList.as_view(),name='TaskList'),
    path('TaskCreate/',TaskCreate.as_view(),name='TaskCreate'),


    re_path('^update/(?P<pk>\d+)/',TaskUpdate.as_view(),name='update'),
    re_path('^delete/(?P<pk>\d+)/',TaskDelete.as_view(),name='delete'),

    
]