from django.shortcuts import render, redirect
from main.core import db, inner_join


# -------- Lazy table access (FIX) --------

def users_table():
    return db.table("users")


def orders_table():
    return db.table("orders")


# -------- Views --------

def list_users(request):
    return render(
        request,
        "users.html",
        {"users": users_table().all()}
    )


def create_user(request):
    if request.method == "POST":
        users_table().insert({
            "id": int(request.POST["id"]),
            "name": request.POST["name"]
        })
        return redirect("/")
    return render(request, "create_user.html")


def update_user(request, user_id):
    if request.method == "POST":
        users_table().update(
            "id",
            int(user_id),
            {"name": request.POST["name"]}
        )
        return redirect("/")

    user = users_table().find("id", int(user_id))
    return render(request, "update_user.html", {"user": user})


def delete_user(request, user_id):
    users_table().delete("id", int(user_id))
    return redirect("/")


def user_orders(request):
    data = inner_join(
        users_table(),
        orders_table(),
        "id",
        "user_id"
    )
    return render(request, "user_orders.html", {"rows": data})

