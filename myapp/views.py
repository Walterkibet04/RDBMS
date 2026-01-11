from django.shortcuts import render, redirect
from main.core import db, inner_join, left_join


# -------- Lazy table access (FIX) --------

def users_table():
    return db.table("users")


def orders_table():
    return db.table("orders")


# -------- Views --------

def list_users(request):
    table = users_table()
    query = request.GET.get("q", "")
    results = table.all()

    if query:
        # search by ID or name
        results = [
            row for row in table.rows
            if query.lower() in str(row["id"]).lower() or query.lower() in row["name"].lower()
        ]

    return render(
        request,
        "users.html",
        {"users": results, "query": query}
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

def list_orders(request):
    table = orders_table()
    query = request.GET.get("q", "")
    results = table.all()

    if query:
        # search by ID, user_id, or amount
        results = [
            row for row in table.rows
            if query.lower() in str(row["id"]).lower()
            or query.lower() in str(row["user_id"]).lower()
            or query.lower() in str(row["amount"]).lower()
        ]

    return render(
        request,
        "orders.html",
        {"orders": results, "query": query}
    )


def create_order(request):
    users = users_table().all()  # get all users

    if request.method == "POST":
        orders_table().insert({
            "id": int(request.POST["id"]),
            "user_id": int(request.POST["user_id"]),
            "amount": int(request.POST["amount"]),
        })
        return redirect("/orders/")

    return render(request, "create_order.html", {"users": users})


def user_orders_left(request):
    """Show all users with their orders (LEFT JOIN)"""
    data = left_join(
        users_table(),
        orders_table(),
        "id",       # left table key
        "user_id"   # right table key
    )
    return render(request, "user_orders_left.html", {"rows": data})