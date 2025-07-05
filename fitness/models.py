from django.db import models
from django.contrib.auth.models import User


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


# User shopping cart to store items before purchase
class Cart(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='cart'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_total_cost(self):
        return sum(item.get_total() for item in self.items.all())

    def __str__(self):
        return f"Cart of {self.user.username}"


# Individual items within a shopping cart
class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE, related_name='items'
    )
    quantity = models.PositiveIntegerField(default=1)
    exercise_plan = models.ForeignKey(
        ExercisePlan, on_delete=models.CASCADE, null=True, blank=True
    )
    nutrition_plan = models.ForeignKey(
        NutritionPlan, on_delete=models.CASCADE, null=True, blank=True
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, null=True, blank=True
    )
    price_at_addition = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        related_items = [self.exercise_plan, self.nutrition_plan, self.product]
        set_items = [item for item in related_items if item is not None]
        if len(set_items) > 1:
            raise ValueError(
                "A CartItem can only be linked to one type of product."
            )

        if not self.price_at_addition:
            if self.exercise_plan:
                self.price_at_addition = self.exercise_plan.price
            elif self.nutrition_plan:
                self.price_at_addition = self.nutrition_plan.price
            elif self.product:
                self.price_at_addition = self.product.price

        super().save(*args, **kwargs)

    def get_item_object(self):
        if self.exercise_plan:
            return self.exercise_plan
        if self.nutrition_plan:
            return self.nutrition_plan
        if self.product:
            return self.product
        return None

    def get_total(self):
        return self.quantity * self.price_at_addition
