from django.urls import path
from .views import *

urlpatterns = [
    path("", list_users),
    path("create/", create_user),
    path("update/<int:user_id>/", update_user),
    path("delete/<int:user_id>/", delete_user),
    path("orders/", user_orders),
]
