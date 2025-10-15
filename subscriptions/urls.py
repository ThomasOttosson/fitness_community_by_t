from django.urls import path
from . import views

urlpatterns = [
    path(
        'subscription/cancel/',
        views.subscription_cancel,
        name='subscription_cancel'
    ),
    # Subscription and dashboard routes.
    path(
        'subscribe/<str:item_type>/<int:pk>/',
        views.create_subscription_checkout,
        name='create_subscription_checkout'
    ),
    path(
        'dashboard/',
        views.subscribed_dashboard,
        name='subscribed_dashboard'
    ),
    path(
        'subscriptions/update/<str:subscription_id>/',
        views.update_subscription,
        name='update_subscription'
    )
]
