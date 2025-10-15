from django.db import models


# Exercise workout plans with pricing and duration
class ExercisePlan(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    duration_weeks = models.PositiveIntegerField()
    stripe_price_id = models.CharField(
        max_length=255, blank=True, null=True, unique=True
    )
    image = models.ImageField(upload_to='plan_images/', blank=True, null=True)

    def __str__(self):
        return self.title


# Nutrition meal plans with pricing and duration
class NutritionPlan(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    duration_weeks = models.PositiveIntegerField()
    stripe_price_id = models.CharField(
        max_length=255, blank=True, null=True, unique=True
    )
    image = models.ImageField(upload_to='plan_images/', blank=True, null=True)

    def __str__(self):
        return self.title
