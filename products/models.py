from django.db import models

from django.contrib.auth.models import User


# Physical products available for purchase
class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    stock = models.PositiveIntegerField()
    image = models.ImageField(
        upload_to='product_images/', blank=True, null=True
    )

    def __str__(self):
        return self.name


# Create your models here.
# User reviews and ratings for products and plans
class Review(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews'
    )
    exercise_plan = models.ForeignKey(
        'fitness.ExercisePlan', on_delete=models.CASCADE, null=True,
        blank=True, related_name='reviews'
    )
    nutrition_plan = models.ForeignKey(
        'fitness.NutritionPlan', on_delete=models.CASCADE, null=True,
        blank=True, related_name='reviews'
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, null=True, blank=True,
        related_name='reviews'
    )
    rating = models.IntegerField(
        choices=[(i, str(i)) for i in range(1, 6)],
        help_text="Rate this item on a scale of 1 to 5."
    )
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        item_name = "Unknown Item"
        if self.exercise_plan:
            item_name = self.exercise_plan.title
        elif self.nutrition_plan:
            item_name = self.nutrition_plan.title
        elif self.product:
            item_name = self.product.name
        return (
            f"Review by {self.user.username} for {item_name} - "
            f"{self.rating} stars"
        )

    def save(self, *args, **kwargs):
        related_items = [self.exercise_plan, self.nutrition_plan, self.product]
        set_items = [item for item in related_items if item is not None]
        if len(set_items) > 1:
            raise ValueError(
                "A Review can only be linked to one type of item "
                "(Exercise Plan, Nutrition Plan, or Product)."
            )
        if not set_items:
            raise ValueError("A Review must be linked to an item.")
        super().save(*args, **kwargs)
