from django.urls import path, include
from .views import *


urlpatterns = [

    path('signup', signup, name="signup"),
    path('index', index, name="index"),
    path('finish', finish, name="finish"),
    path('', base, name="home"),
    path('history', history, name="history")
    # path('create_criteria_normal', create_criteria_normal, name='create_criteria_normal'),

]
