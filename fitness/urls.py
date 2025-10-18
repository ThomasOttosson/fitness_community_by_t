from django.urls import path
from . import views

# Define the URL patterns for the application.
urlpatterns = [
    # Route for the homepage.
    path('', views.home, name='home'),

    # Routes for listing and viewing exercise plans.
    path(
        'exercise-plans/',
        views.exercise_plan_list,
        name='exercise_plan_list'
    ),
    path(
        'exercise-plans/<int:pk>/',
        views.exercise_plan_detail,
        name='exercise_plan_detail'
    ),
    # Route to display specific content for an exercise plan.
    path(
        'exercise-plans/<int:pk>/content/',
        views.exercise_plan_content,
        name='exercise_plan_content'
    ),

    # Routes for listing and viewing nutrition plans.
    path(
        'nutrition-plans/',
        views.nutrition_plan_list,
        name='nutrition_plan_list'
    ),
    path(
        'nutrition-plans/<int:pk>/',
        views.nutrition_plan_detail,
        name='nutrition_plan_detail'
    ),
    # Route to display specific content for a nutrition plan.
    path(
        'nutrition-plans/<int:pk>/content/',
        views.nutrition_plan_content,
        name='nutrition_plan_content'
    ),


    # User account and order history routes.
    path('register/', views.register, name='register'),
    path('accounts/profile/', views.profile, name='profile'),

    # Newsletter signup route.
    path(
        'newsletter/signup/',
        views.newsletter_signup,
        name='newsletter_signup'
    ),

    # Staff-specific dashboard route.
    path('staff-dashboard/', views.staff_dashboard, name='staff_dashboard'),
]
