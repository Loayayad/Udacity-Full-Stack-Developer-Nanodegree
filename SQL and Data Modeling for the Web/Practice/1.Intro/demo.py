import psycopg2

conn = psycopg2.connect('dbname=example user=postgres password=1234')

cursor = conn.cursor()

# Open a cursor to perform database operations
cur = conn.cursor()

# drop any existing todos table
#cur.execute("DROP TABLE IF EXISTS todos;")

# (re)create the todos table
# (note: triple quotes allow multiline text in python)
cur.execute('''
  CREATE TABLE table2 (
    id INTEGER PRIMARY KEY,
    completed BOOLEAN NOT NULL DEFAULT FALSE
  );
''')

cursor.execute('INSERT INTO table2 (id, completed) VALUES (1,true);')

# commit, so it does the executions on the db and persists in the db
conn.commit()

cur.close()
conn.close()