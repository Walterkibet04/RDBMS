import json
import os

# -------------------------------
# Paths
# -------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_FILE = os.path.join(BASE_DIR, "db.json")


# -------------------------------
# Table Class
# -------------------------------
class Table:
    def __init__(self, name, columns, types, pk=None, unique=None):
        self.name = name
        self.columns = columns
        self.types = types

        self.primary_key = pk
        self.unique = unique or []

        self.rows = []
        self.indexes = {}
        self.database = None  # set when table added to Database

        # Initialize indexes for primary key and unique columns
        for col in [self.primary_key] + self.unique:
            if col:
                self.indexes[col] = {}

    # -------------------------------
    # Link table to database
    # -------------------------------
    def set_database(self, db):
        self.database = db

    # -------------------------------
    # Validation
    # -------------------------------
    def _type_check(self, row):
        for col, val in row.items():
            expected = self.types[col]
            if expected == "INT" and not isinstance(val, int):
                raise Exception(f"{col} must be INT")
            if expected == "TEXT" and not isinstance(val, str):
                raise Exception(f"{col} must be TEXT")

    def _check_unique(self, row, ignore_row=None):
        for col in self.indexes:
            val = row[col]
            existing = self.indexes[col].get(val)
            if existing and existing is not ignore_row:
                raise Exception(f"Duplicate value for {col}")

    # -------------------------------
    # CRUD Operations
    # -------------------------------
    def insert(self, row):
        self._type_check(row)
        self._check_unique(row)

        self.rows.append(row)

        # Update indexes
        for col, index in self.indexes.items():
            index[row[col]] = row

        # Auto-save
        if self.database:
            self.database.save()

    def all(self):
        return self.rows

    def find(self, col, value):
        if col in self.indexes:
            return self.indexes[col].get(value)
        for r in self.rows:
            if r[col] == value:
                return r
        return None

    def update(self, where_col, where_val, updates):
        row = self.find(where_col, where_val)
        if not row:
            raise Exception("Row not found")

        # Build new row candidate
        new_row = row.copy()
        new_row.update(updates)

        # Validate
        self._type_check(new_row)
        self._check_unique(new_row, ignore_row=row)

        # Remove old index entries
        for col in self.indexes:
            self.indexes[col].pop(row[col], None)

        # Apply updates
        row.update(updates)

        # Re-add to indexes
        for col in self.indexes:
            self.indexes[col][row[col]] = row

        # Auto-save
        if self.database:
            self.database.save()

    def delete(self, where_col, where_val):
        row = self.find(where_col, where_val)
        if not row:
            raise Exception("Row not found")

        self.rows.remove(row)

        for col in self.indexes:
            self.indexes[col].pop(row[col], None)

        # Auto-save
        if self.database:
            self.database.save()


# -------------------------------
# Database Class
# -------------------------------
class Database:
    def __init__(self, file=DB_FILE):
        self.tables = {}
        self.file = file
        self.load()
        self._init_empty_tables()

    # Load tables from JSON
    def load(self):
        if not os.path.exists(self.file):
            return
        with open(self.file, "r") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                return
        for name, info in data.items():
            table = Table(
                name,
                info["columns"],
                info["types"],
                pk=info.get("primary_key"),
                unique=info.get("unique", [])
            )
            table.rows = info.get("rows", [])

            # rebuild indexes
            for col, index in table.indexes.items():
                for row in table.rows:
                    index[row[col]] = row

            # link to this database
            table.set_database(self)

            self.tables[name] = table

    # Save tables to JSON
    def save(self):
        data = {}
        for name, table in self.tables.items():
            data[name] = {
                "columns": table.columns,
                "types": table.types,
                "primary_key": table.primary_key,
                "unique": table.unique,
                "rows": table.rows
            }
        with open(self.file, "w") as f:
            json.dump(data, f, indent=2)

    # Ensure default tables exist
    def _init_empty_tables(self):
        if "users" not in self.tables:
            self.create_table(
                name="users",
                columns=["id", "name"],
                types={"id": "INT", "name": "TEXT"},
                pk="id"
            )
        if "orders" not in self.tables:
            self.create_table(
                name="orders",
                columns=["id", "user_id", "amount"],
                types={"id": "INT", "user_id": "INT", "amount": "INT"},
                pk="id"
            )

    # Create a new table
    def create_table(self, name, columns, types, pk=None, unique=None):
        if name in self.tables:
            raise Exception(f"Table {name} already exists")

        table = Table(
            name=name,
            columns=columns,
            types=types,
            pk=pk,
            unique=unique,
        )
        # link table to db
        table.set_database(self)
        self.tables[name] = table
        self.save()

    # Access table by name
    def table(self, name):
        return self.tables[name]


# -------------------------------
# JOIN FUNCTIONS
# -------------------------------
def inner_join(left_table, right_table, left_key, right_key):
    result = []
    right_index = {}
    for row in right_table.rows:
        right_index.setdefault(row[right_key], []).append(row)

    for lrow in left_table.rows:
        matches = right_index.get(lrow[left_key])
        if matches:
            for rrow in matches:
                merged = {f"user_{k}": v for k, v in lrow.items()}
                merged.update({f"order_{k}": v for k, v in rrow.items()})
                result.append(merged)
    return result


def left_join(left_table, right_table, left_key, right_key):
    result = []
    right_index = {}
    for row in right_table.rows:
        right_index.setdefault(row[right_key], []).append(row)

    for lrow in left_table.rows:
        matches = right_index.get(lrow[left_key])
        if matches:
            for rrow in matches:
                merged = {f"user_{k}": v for k, v in lrow.items()}
                merged.update({f"order_{k}": v for k, v in rrow.items()})
                result.append(merged)
        else:
            nulls = {k: None for k in right_table.columns}
            merged = {f"user_{k}": v for k, v in lrow.items()}
            merged.update({f"order_{k}": v for k, v in nulls.items()})
            result.append(merged)
    return result


# -------------------------------
# GLOBAL DATABASE INSTANCE
# -------------------------------
db = Database(DB_FILE)

