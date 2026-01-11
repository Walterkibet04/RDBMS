from main.sql import execute

print("MiniRDBMS REPL (type exit to quit)")

while True:
    q = input("sql> ")
    if q.lower() == "exit":
        break
    try:
        result = execute(q)
        if isinstance(result, list):
            for r in result:
                print(r)
        else:
            print(result)
    except Exception as e:
        print("Error:", e)
