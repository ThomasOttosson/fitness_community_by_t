from django.db import models
from django.contrib.auth.models import User
from fitness.models import ExercisePlan, NutritionPlan
from products.models import Product


# Create your models here.
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


