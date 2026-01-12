# **Overview**

MiniRDBMS is a relational database management system implemented in Python.
It supports basic SQL-like commands, an interactive REPL, disk persistence, and a Django web UI to demonstrate CRUD operations and joins.
The project is designed to illustrate core database concepts without using an existing database engine or ORM.

## **Features**
* Tables & schema	✅
* CRUD operations	✅
* Primary keys	✅
* Unique constraints	✅
* Indexes	✅
* JOINs	✅
* SQL-like interface	✅
* Interactive REPL	✅
* Disk persistence	✅
* Web app demonstration	✅


## **Architecture**

RDBMS/

├── main/

│   ├── core.py       # Database backbone

│   ├── sql.py        # SQL-like query parser

│   ├── repl.py       # Interactive REPL

│
├── myapp/

│   ├── views.py      # Django UI logic

│   ├── templates/    # HTML templates

│

├── db.json           # Persistent storage

└── manage.py

## **Core Components**

### Database Engine (core.py)

* Manages tables and persistence
* Enforces schema, types, primary keys, and uniqueness
* Implements cascading deletes
* Stores data in memory and writes to db.json

### **SQL Interface (sql.py)**
Supports commands such as:

*CREATE TABLE users (id INT PRIMARY KEY, name TEXT);*

*INSERT INTO users VALUES 1 Walter*

*SELECT \* FROM users WHERE id=1*

*UPDATE users SET name=Alice WHERE id=1*

*DELETE FROM users WHERE id=1*

*SELECT \* FROM users JOIN orders ON users.id = orders.user\_id*

## **REPL**

Run:

*python -m main.repl*

Provides an interactive SQL-like interface backed by the same database used by the UI.

## **Django Web App**

The Django app demonstrates:

* User and Order CRUD
* Search (SELECT WHERE)
* INNER JOIN and LEFT JOIN views
* Foreign key selection via dropdowns

⚠️ The Django server loads the database at startup.

If data is modified via the REPL, restart the server to reflect changes.

**Persistence**

All data is stored in db.json.

* Writes are saved immediately
* Data survives server restarts
* REPL and UI share the same storage

**Conclusion**
MiniRDBMS demonstrates how a relational database works internally, including schema enforcement, indexing, joins, persistence, interactive repl and UI integration — all implemented from scratch.
