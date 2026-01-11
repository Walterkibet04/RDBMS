from django.urls import path
from .api import *

urlpatterns = [
    path("users/", users_api),
    path("users/<int:user_id>/", user_detail_api),
    path("orders/", orders_api),
    path("user-orders/", user_orders_api),
]
