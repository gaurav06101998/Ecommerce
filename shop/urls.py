from django.urls import path
from django.contrib.auth import views as auth_views  # Import built-in authentication views
from . import views


app_name = 'shop'

urlpatterns = [
    path('', views.product_list, name='product_list'),  # Homepage showing product list
    path('product/<int:id>/', views.product_detail, name='product_detail'),  # Product detail page
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_detail, name='cart_detail'),  # View cart details
    path('checkout/', views.checkout, name='checkout'),  # Checkout page
    path('signup/', views.signup, name='signup'),  # Signup for new users
    path('login/', views.user_login, name='login'),  # Custom login view
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),  # Built-in logout view
    path('profile/', views.profile, name='profile'),  # Profile URL
    path('search/', views.product_search, name='search'),  # Search URL
    path('product_list/', views.product_list, name='product_list'),  # Other paths
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),


]
