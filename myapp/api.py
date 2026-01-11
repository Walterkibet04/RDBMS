from rest_framework.decorators import api_view
from rest_framework.response import Response
from main.core import db, inner_join

users = db.table("users")
orders = db.table("orders")


@api_view(["GET", "POST"])
def users_api(request):
    if request.method == "GET":
        return Response(users.all())

    users.insert({
        "id": int(request.data["id"]),
        "name": request.data["name"]
    })
    return Response({"status": "created"}, status=201)


@api_view(["PUT", "DELETE"])
def user_detail_api(request, user_id):
    if request.method == "PUT":
        users.update("id", user_id, {"name": request.data["name"]})
        return Response({"status": "updated"})

    users.delete("id", user_id)
    return Response({"status": "deleted"})


@api_view(["GET", "POST"])
def orders_api(request):
    if request.method == "GET":
        return Response(orders.all())

    orders.insert({
        "id": int(request.data["id"]),
        "user_id": int(request.data["user_id"]),
        "product": request.data["product"]
    })
    return Response({"status": "created"}, status=201)


@api_view(["GET"])
def user_orders_api(request):
    return Response(inner_join(users, orders, "id", "user_id"))
