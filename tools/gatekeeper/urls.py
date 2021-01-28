from django.urls import path, include
from . import views

urlpatterns = [
    path('knock-on-door', views.index),
    path('dashboard', views.dashboard, name='dashboard'),
    path('logout', views.logout, name='logout'),
    path('', include('django.contrib.auth.urls')),
    path('', include('social_django.urls')),
]
