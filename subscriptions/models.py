from django.db import models
from django.contrib.auth.models import User
from fitness.models import ExercisePlan, NutritionPlan


# Create your models here.
# User subscriptions to recurring plans
class Subscription(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='subscriptions'
    )
    exercise_plan = models.ForeignKey(
        ExercisePlan, on_delete=models.SET_NULL, null=True, blank=True
    )
    nutrition_plan = models.ForeignKey(
        NutritionPlan, on_delete=models.SET_NULL, null=True, blank=True
    )
    stripe_subscription_id = models.CharField(
        max_length=255, unique=True, blank=True, null=True
    )
    stripe_customer_id = models.CharField(
        max_length=255, blank=True, null=True
    )
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('user', 'exercise_plan', 'nutrition_plan')

    def __str__(self):
        plan_name = "Unknown Plan"
        if self.exercise_plan:
            plan_name = self.exercise_plan.title
        elif self.nutrition_plan:
            plan_name = self.nutrition_plan.title
        return (
            f"{self.user.username}'s subscription to {plan_name} "
            f"(Active: {self.is_active})"
        )

    def save(self, *args, **kwargs):
        related_plans = [self.exercise_plan, self.nutrition_plan]
        set_plans = [plan for plan in related_plans if plan is not None]
        if len(set_plans) > 1:
            raise ValueError(
                "A Subscription can only be linked to one type of plan "
                "(Exercise or Nutrition)."
            )
        super().save(*args, **kwargs)
