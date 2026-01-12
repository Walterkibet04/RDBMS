from main.core import db, inner_join, left_join


def execute(query: str):
    query = query.strip().rstrip(";")
    tokens = query.split()
    cmd = tokens[0].upper()

    if cmd == "CREATE":
        return _create_table(query)

    if cmd == "INSERT":
        return _insert(query)

    if cmd == "SELECT":
        return _select(query)

    if cmd == "UPDATE":
        return _update(query)

    if cmd == "DELETE":
        return _delete(query)

    raise Exception("Unsupported SQL")


# -------------------------
# CREATE TABLE
# -------------------------

def _create_table(query):
    # CREATE TABLE users (id INT PRIMARY KEY, name TEXT)
    name = query.split()[2]
    cols_part = query[query.index("(") + 1: query.index(")")]

    columns = []
    types = {}
    pk = None
    unique = []

    for col in cols_part.split(","):
        parts = col.strip().split()
        col_name = parts[0]
        col_type = parts[1]

        columns.append(col_name)
        types[col_name] = col_type

        if "PRIMARY" in parts:
            pk = col_name
        if "UNIQUE" in parts:
            unique.append(col_name)

    db.create_table(name, columns, types, pk, unique)
    return f"Table '{name}' created"


# -------------------------
# INSERT
# -------------------------

def _insert(query):
    # INSERT INTO users VALUES 1 Alice
    parts = query.split()
    table = db.table(parts[2])
    values = [_parse(v) for v in parts[4:]]
    row = dict(zip(table.columns, values))
    table.insert(row)
    return "Inserted"


# -------------------------
# SELECT + JOIN
# -------------------------

def _select(query):
    tokens = query.split()

    # -------------------------------
    # SELECT * FROM table
    # -------------------------------
    if (
        len(tokens) == 4
        and tokens[0] == "SELECT"
        and tokens[1] == "*"
        and tokens[2] == "FROM"
    ):
        table = db.table(tokens[3])
        return table.all()

    # -------------------------------
    # SELECT * FROM table WHERE col=value
    # -------------------------------
    if "WHERE" in tokens and "JOIN" not in tokens:
        table = db.table(tokens[3])
        where_index = tokens.index("WHERE")
        col, val = tokens[where_index + 1].split("=")

        val = _parse(val)
        return [row for row in table.rows if row[col] == val]

    # -------------------------------
    # SELECT * FROM A LEFT JOIN B ON A.x = B.y
    # -------------------------------
    if "LEFT" in tokens and "JOIN" in tokens:
        left = tokens[3]
        right = tokens[6]
        left_key = tokens[8].split(".")[1]
        right_key = tokens[10].split(".")[1]

        return left_join(
            db.table(left),
            db.table(right),
            left_key,
            right_key
        )

    # -------------------------------
    # SELECT * FROM A JOIN B ON A.x = B.y
    # -------------------------------
    if "JOIN" in tokens:
        left = tokens[3]
        right = tokens[5]
        left_key = tokens[7].split(".")[1]
        right_key = tokens[9].split(".")[1]

        return inner_join(
            db.table(left),
            db.table(right),
            left_key,
            right_key
        )

    raise Exception("Unsupported SELECT query")




# -------------------------
# UPDATE
# -------------------------

def _update(query):
    # UPDATE users SET name=Bob WHERE id=1
    tokens = query.split()

    table_name = tokens[1]
    table = db.table(table_name)

    set_index = tokens.index("SET")
    where_index = tokens.index("WHERE")

    set_col, set_val = tokens[set_index + 1].split("=")
    where_col, where_val = tokens[where_index + 1].split("=")

    table.update(
        where_col,
        _parse(where_val),
        {set_col: _parse(set_val)}
    )

    return "Updated"



# -------------------------
# DELETE
# -------------------------

def _delete(query):
    # DELETE FROM orders WHERE id=1
    tokens = query.split()

    table_name = tokens[tokens.index("FROM") + 1]
    table = db.table(table_name)

    where_index = tokens.index("WHERE")
    where_col, where_val = tokens[where_index + 1].split("=")

    table.delete(where_col, _parse(where_val))

    return "Deleted"



def _parse(value):
    if value.isdigit():
        return int(value)
    return value
