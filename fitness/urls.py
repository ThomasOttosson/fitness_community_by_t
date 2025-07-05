from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path(
        'exercise-plans/',
        views.exercise_plan_list,
        name='exercise_plan_list'
    ),
    path(
        'nutrition-plans/',
        views.nutrition_plan_list,
        name='nutrition_plan_list'
    ),