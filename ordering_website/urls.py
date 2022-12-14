from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.main_page, name="main"),
    path("home", views.home, name="home"),
    path('registration', views.registration_page, name="registration"),
    path('login', views.login_page, name="login"),
    path('logout', views.logout, name="logout"),
    path('profile', views.profile, name="profile"),
    path('cart_page', views.cart_page, name="cart_page"),
    path('add_to_cart/<int:wine_id>/', views.add_to_cart, name="add_to_cart"),
    path('remove_from_cart/<int:wine_id>/', views.remove_from_cart, name="remove_from_cart"),
    path('wine_page/<int:wine_id>/', views.wine_page, name="wine_page"),
    path('add_wine_page', views.add_wine_page, name="add_wine_page"),
    path('update_wine_page/<int:wine_id>/', views.update_wine_page, name="update_wine_page"),
    path('load/<int:wine_id>/', views.load_more, name="load"),
    path('checkout_page', views.checkout_page, name="checkout_page"),
    path('users', views.users, name="users"),
    path('all_wines', views.all_wines, name="all_wines"),
    path('remove_user/<uuid:user_uid>/', views.remove_user, name="remove_user"),
    path('switch_admin_user/<uuid:user_uid>/', views.switch_admin_user, name="switch_admin_user"),
    path('remove_wine/<int:wine_id>/', views.remove_wine, name="remove_wine"),
    path('remove_opinion/<int:wine_id>/<uuid:user_uid>', views.remove_opinion, name="remove_opinion"),
    path('orders', views.orders, name="orders"),
    path('check_order/<str:order_id>/', views.check_order, name="check_order"),
    path('cancel_order/<str:order_id>/', views.cancel_order, name="cancel_order"),
    path('update_order_status/<str:order_id>/<str:status>/', views.update_order_status, name="update_order_status"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
