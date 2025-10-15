from django.urls import path
from . import views


urlpatterns = [
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
    path('', views.checkout, name='checkout'),
    path('payment-success/', views.payment_success, name='payment_success'),
    path(
        'order-confirmation/',
        views.order_confirmation,
        name='order_confirmation'
    ),
    path('accounts/orders/', views.order_history, name='order_history'),
]
