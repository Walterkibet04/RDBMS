from main.core import db


def init_schema():
    if "users" not in db.tables:
        db.create_table(
            "users",
            ["id", "name"],
            {"id": "INT", "name": "TEXT"},
            "id",          # primary key (positional)
            []             # unique keys
        )

    if "orders" not in db.tables:
        db.create_table(
            "orders",
            ["id", "user_id", "amount"],
            {"id": "INT", "user_id": "INT", "amount": "INT"},
            "id",          # primary key
            []
        )
