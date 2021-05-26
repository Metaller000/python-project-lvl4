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
]
