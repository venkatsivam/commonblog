import sqlite3
import datetime

connection = sqlite3.connect("blog.db")
# print("Opened successfully")
cursor = connection.cursor()
# cursor.execute('''DROP TABLE user;''')
# cursor.execute('''DROP TABLE blog;''')
# cursor.execute('''DROP TABLE comment;''')
# cursor.execute('''DROP TABLE response;''')


cursor.execute(
    "create table user(id INTEGER PRIMARY KEY AUTOINCREMENT,username TEXT UNIQUE NOT NULL,email TEXT UNIQUE NOT NULL,password TEXT NOT NULL)")
cursor.execute(
    "create table blog(id INTEGER PRIMARY KEY AUTOINCREMENT, name VARCHAR(255), content TEXT, author INTEGER,created_date TIMESTAMP, modified_date TIMESTAMP, FOREIGN KEY(author) REFERENCES user(id))")
cursor.execute(
    "create table comment(id INTEGER PRIMARY KEY AUTOINCREMENT, blog INTEGER,user INTEGER,comment TEXT, created_date TIMESTAMP, modified_date TIMESTAMP, FOREIGN KEY(blog) REFERENCES blog(id), FOREIGN KEY(user) REFERENCES user(id) )")
cursor.execute(
    "create table response(id INTEGER PRIMARY KEY AUTOINCREMENT,blog INTEGER,user INTEGER, like_or_not BOOL,response_date TIMESTAMP,FOREIGN KEY(blog) REFERENCES blog(id), FOREIGN KEY(user) REFERENCES user(id))")
print("Tables created successfully")
connection.close()
