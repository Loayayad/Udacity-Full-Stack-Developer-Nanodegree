import psycopg2

conn = psycopg2.connect('dbname=example user=postgres password=1234')


# Open a cursor to perform database operations
cursor = conn.cursor()

# drop any existing todos table
cursor.execute("DROP TABLE IF EXISTS table2;")

# (re)create the todos table
# (note: triple quotes allow multiline text in python)
cursor.execute('''
  CREATE TABLE table2 (
    id INTEGER PRIMARY KEY,
    completed BOOLEAN NOT NULL DEFAULT FALSE
  );
''')

SQL = 'INSERT INTO table2 (id, completed) VALUES (%(id)s,%(completed)s);'
data = {
    'id': 2,
    'completed': False
}

cursor.execute('INSERT INTO table2 (id, completed) VALUES (%s,%s);', (1, True))

# cursor.execute('INSERT INTO table2 (id, completed) VALUES (%(id)s,%(completed)s);', {
#    'id': 2,'completed': False})

cursor.execute(SQL, data)

cursor.execute('INSERT INTO table2 (id, completed) VALUES (%s,%s);', (3, True))

cursor.execute('SELECT * from table2;')
result = cursor.fetchmany(2)
print('fetchmany(2)', result)

result2 = cursor.fetchone()
print('fetchone', result2)

result3 = cursor.fetchone()
print('fetchone', result3)


# commit, so it does the executions on the db and persists in the db
conn.commit()

cursor.close()
conn.close()
