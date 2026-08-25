import sqlite3
from werkzeug.security import generate_password_hash

conn = sqlite3.connect('c:/Users/kooki/Desktop/Farm/instance/autonomous_farmer.db')
cursor = conn.cursor()
password_hash = generate_password_hash('password')
cursor.execute("UPDATE users SET password_hash=? WHERE email='user@example.com'", (password_hash,))
conn.commit()
print("Successfully reset user@example.com password to 'password'. Row count affected:", cursor.rowcount)
conn.close()
