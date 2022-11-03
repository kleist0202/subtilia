from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path('registration', views.registration_page, name="registration"),
    path('login', views.login_page, name="login"),
    path('logout', views.logout, name="logout"),
    path('profile', views.profile, name="profile"),
    path('cart_page', views.cart_page, name="cart_page"),
    path('add_to_cart/<int:wine_id>/', views.add_to_cart, name="add_to_cart"),
    path('remove_from_cart/<int:wine_id>/', views.remove_from_cart, name="remove_from_cart"),
]
