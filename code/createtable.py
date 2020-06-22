import sqlite3

connection=sqlite3.connect("database.db")
cursor=connection.cursor()


query="CREATE TABLE users (id INTEGER PRIMARY KEY ,username text , password text)"
cursor.execute(query)
connection.commit()


query="CREATE TABLE items (name text , price real)"
cursor.execute(query)
connection.commit()


connection.close()