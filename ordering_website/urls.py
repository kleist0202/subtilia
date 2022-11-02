from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path('registration', views.registration_page, name="registration"),
    path('login', views.login_page, name="login"),
    path('logout', views.logout, name="logout"),
    path('profile', views.profile, name="profile"),
]
