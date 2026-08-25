import sqlite3
from werkzeug.security import check_password_hash

conn = sqlite3.connect('c:/Users/kooki/Desktop/Farm/instance/autonomous_farmer.db')
cursor = conn.cursor()
cursor.execute("SELECT password_hash FROM users WHERE email='user@example.com'")
row = cursor.fetchone()
if row:
    print("Match 'password':", check_password_hash(row[0], 'password'))
    print("Match 'password_new':", check_password_hash(row[0], 'password_new'))
else:
    print("User not found.")
conn.close()
