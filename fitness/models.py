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

    def __str__(self):
        item_name = "Unknown Item"
        if self.exercise_plan:
            item_name = self.exercise_plan.title
        elif self.nutrition_plan:
            item_name = self.nutrition_plan.title
        elif self.product:
            item_name = self.product.name
        return f"{self.quantity} x {item_name} in Cart {self.cart.id}"


# Completed purchases with payment tracking
class Order(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='orders'
    )
    order_date = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    stripe_payment_intent_id = models.CharField(
        max_length=255, unique=True, blank=True, null=True
    )

    class Meta:
        ordering = ['-order_date']

    def __str__(self):
        return (
            f"Order {self.id} by {self.user.username} on "
            f"{self.order_date.strftime('%Y-%m-%d')}"
        )


# Individual items within completed orders
class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name='items'
    )
    item_type = models.CharField(max_length=50)
    item_id = models.PositiveIntegerField()
    item_name = models.CharField(max_length=200)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.item_name} for Order {self.order.id}"

    def get_total(self):
        return self.quantity * self.price


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


# User reviews and ratings for products and plans
class Review(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews'
    )
    exercise_plan = models.ForeignKey(
        ExercisePlan, on_delete=models.CASCADE, null=True, blank=True,
        related_name='reviews'
    )
    nutrition_plan = models.ForeignKey(
        NutritionPlan, on_delete=models.CASCADE, null=True, blank=True,
        related_name='reviews'
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
