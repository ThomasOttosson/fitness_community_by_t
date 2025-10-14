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

    # Routes for listing and viewing products.
    path('products/', views.product_list, name='product_list'),
    path(
        'products/<int:pk>/',
        views.product_detail,
        name='product_detail'
    ),

    # Cart management routes.
    path(
        'add-to-cart/<str:item_type>/<int:pk>/',
        views.add_to_cart,
        name='add_to_cart'
    ),
    path('cart/', views.cart_detail, name='cart_detail'),
    path(
        'cart/update/<int:item_id>/',
        views.update_cart_item,
        name='update_cart_item'
    ),
    path(
        'cart/remove/<int:item_id>/',
        views.remove_from_cart,
        name='remove_from_cart'
    ),

    # Checkout and payment processing routes.
    path('checkout/', views.checkout, name='checkout'),
    path('payment-success/', views.payment_success, name='payment_success'),
    path(
        'order-confirmation/',
        views.order_confirmation,
        name='order_confirmation'
    ),

    # User account and order history routes.
    path('accounts/orders/', views.order_history, name='order_history'),
    path('register/', views.register, name='register'),
    path('accounts/profile/', views.profile, name='profile'),

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

    # Newsletter signup route.
    path(
        'newsletter/signup/',
        views.newsletter_signup,
        name='newsletter_signup'
    ),

    # Staff-specific dashboard route.
    path('staff-dashboard/', views.staff_dashboard, name='staff_dashboard'),
    path('review/<int:pk>/edit/', views.edit_review, name='edit_review'),
    path('review/<int:pk>/delete/', views.delete_review, name='delete_review'),
]
