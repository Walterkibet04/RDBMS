class Table:
    def __init__(self, name, columns, types, pk=None, unique=None):
        self.name = name
        self.columns = columns
        self.types = types
        self.pk = pk
        self.unique = unique or []
        self.rows = []
        self.indexes = {}

        for col in [pk] + self.unique:
            if col:
                self.indexes[col] = {}

    def _type_check(self, row):
        for col, val in row.items():
            expected = self.types[col]
            if expected == "INT" and not isinstance(val, int):
                raise Exception(f"{col} must be INT")
            if expected == "TEXT" and not isinstance(val, str):
                raise Exception(f"{col} must be TEXT")

    def insert(self, row):
        self._type_check(row)

        for col, index in self.indexes.items():
            if row[col] in index:
                raise Exception(f"Duplicate value for {col}")

        self.rows.append(row)

        for col, index in self.indexes.items():
            index[row[col]] = row

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

        for k, v in updates.items():
            row[k] = v

    def delete(self, where_col, where_val):
        row = self.find(where_col, where_val)
        if not row:
            raise Exception("Row not found")

        self.rows.remove(row)

        for col, index in self.indexes.items():
            index.pop(row[col], None)


class Database:
    def __init__(self):
        self.tables = {}

    def create_table(self, name, columns, types, pk=None, unique=None):
        self.tables[name] = Table(name, columns, types, pk, unique)

    def table(self, name):
        return self.tables[name]


def inner_join(left, right, left_key, right_key):
    result = []
    for l in left.rows:
        for r in right.rows:
            if l[left_key] == r[right_key]:
                result.append({**l, **r})
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
                result.append({**lrow, **rrow})
        else:
            # no match → NULLs for right table
            nulls = {col: None for col in right_table.columns}
            result.append({**lrow, **nulls})

    return result

# GLOBAL DATABASE INSTANCE
db = Database()

# db.create_table(
#     "users",
#     columns=["id", "name"],
#     types={"id": "INT", "name": "TEXT"},
#     pk="id",
#     unique=["name"]
# )

# db.create_table(
#     "orders",
#     columns=["id", "user_id", "product"],
#     types={"id": "INT", "user_id": "INT", "product": "TEXT"},
#     pk="id"
# )

