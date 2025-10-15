from django.urls import path
from . import views

urlpatterns = [
    # Routes for listing and viewing products.
    path('', views.product_list, name='product_list'),
    path(
        '<int:pk>/',
        views.product_detail,
        name='product_detail'
    ),
    path('<int:pk>/edit/', views.edit_review, name='edit_review'),
    path('<int:pk>/delete/', views.delete_review, name='delete_review'),  
]
