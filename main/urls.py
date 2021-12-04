from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('register', views.register, name="register"),
    path('action/register', views.register_action, name="register_action"),
    path('action/login', views.login_action, name="login_action"),
    path('action/logout', views.logout_action, name="logout_action"),
    path('action/order/add', views.addorder_action, name="addorder_action"),
    path('action/order/remove', views.rmorder_action, name="rmorder_action"),
    path('action/order/edit', views.editorder_action, name="editorder_action"),
    path('user_panel', views.user_panel, name="user_panel"),
    path('user_panel/order/add', views.up_add_order, name="up_add_order"),
    path('user_panel/order/edit', views.up_edit_order, name="up_edit_order"),
    path('user_panel/password/edit', views.up_edit_password, name="up_edit_password"),
    path('user_panel/personal_info/edit', views.up_edit_personal_info, name="up_edit_personal_info"),
]
