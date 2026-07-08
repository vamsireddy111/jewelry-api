from django.urls import path
from . import views

urlpatterns = [
    # Products
    path('products/', views.get_products),
    path('products/add/', views.add_product),
    path('products/<int:id>/', views.update_product),

    # Categories
    path('categories/', views.get_categories),
    path('categories/<int:id>/products/', views.get_products_by_category),

    # Users
    path('users/register/', views.register_user),
    path('users/login/', views.login_user),
    path('', views.home),
]