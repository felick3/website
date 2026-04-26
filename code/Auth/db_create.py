import sqlite3

# Connecting creates the file automatically if it doesn't exist
conn = sqlite3.connect('Users.db')
cursor = conn.cursor()

# Create a table
cursor.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, password TEXT, email TEXT)''')

# Save changes and close
conn.commit()
conn.close()
