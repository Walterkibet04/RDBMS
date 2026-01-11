from django.urls import path
from .views import *

urlpatterns = [
    path("", list_users),
    path("users/create/", create_user),
    path("users/update/<int:user_id>/", update_user),
    path("users/delete/<int:user_id>/", delete_user),
    path("orders/create/", create_order),
    path("orders/", list_orders),
    path("join/", user_orders),
    path("join-left/", user_orders_left),
]
