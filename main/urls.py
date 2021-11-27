from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('register', views.register, name="register"),
    path('action/register', views.register_action, name="register_action"),
    path('action/login', views.login_action, name="login_action"),
    path('action/logout', views.logout_action, name="logout_action"),
    path('user_panel', views.user_panel, name="user_panel"),
    path('user_panel/change_password', views.up_change_password, name="up_change_password"),
    path('user_panel/add_order', views.up_add_order, name="up_add_order"),
]
