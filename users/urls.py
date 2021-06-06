# from django.conf.urls import url
from django.urls import path, include
from users import views

import users

urlpatterns = [    
    path('', include('django.contrib.auth.urls')),    
    path('', views.base),
    path('users/', views.users),
    path('users/create/', views.create),
    path('users/<int:pk>/update/', views.update),
    path('users/<int:pk>/delete/', views.delete),
    path('statuses/', views.statuses_read),
    path('statuses/create/', views.statuses_create),
    path('statuses/<int:pk>/update/', views.statuses_update),
    path('statuses/<int:pk>/delete/', views.statuses_delete),
]
