from django.contrib import admin
from .models import (
    ExercisePlan,
    NutritionPlan
)


# Register models with the Django admin site for management.
admin.site.register(ExercisePlan)
admin.site.register(NutritionPlan)
