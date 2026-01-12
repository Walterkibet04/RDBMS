from django.shortcuts import render, redirect
from main.core import db, inner_join, left_join


# -------- Lazy table access (FIX) --------

def users_table():
    db.reload()
    return db.table("users")


def orders_table():
    db.reload()
    return db.table("orders")


# -------- Views --------

def list_users(request):
    db.reload()
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
    db.reload()
    if request.method == "POST":
        users_table().insert({
            "id": int(request.POST["id"]),
            "name": request.POST["name"]
        })
        return redirect("/")
    return render(request, "create_user.html")


def update_user(request, user_id):
    db.reload()
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
    db.reload()
    users_table().delete("id", int(user_id))
    return redirect("/")


def user_orders(request):
    db.reload()
    rows = inner_join(
        users_table(),
        orders_table(),
        "id",
        "user_id"
    )

    q = request.GET.get("q", "").lower()

    if q:
        rows = [
            r for r in rows
            if q in str(r["user_id"]).lower()
            or q in r["user_name"].lower()
            or q in str(r["order_id"]).lower()
            or q in str(r["order_amount"]).lower()
        ]

    return render(
        request,
        "user_orders.html",
        {"rows": rows, "query": q}
    )


def list_orders(request):
    db.reload()
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
    db.reload()
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
    db.reload()
    rows = left_join(
        users_table(),
        orders_table(),
        "id",
        "user_id"
    )

    q = request.GET.get("q", "").lower()

    if q:
        rows = [
            r for r in rows
            if q in str(r["user_id"]).lower()
            or q in r["user_name"].lower()
            or q in str(r["order_id"]).lower()
            or q in str(r["order_amount"]).lower()
        ]

    return render(
        request,
        "user_orders_left.html",
        {"rows": rows, "query": q}
    )
