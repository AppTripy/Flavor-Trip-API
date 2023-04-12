from flask import Flask, request, jsonify
import mariadb
import sys
import bcrypt

app = Flask(__name__)

# Database configuration
config = {
    'host': 'localhost',
    'port': 3306,
    'user': 'uroot',
    'password': 'proot',
    'database': 'flavor_trip_db'
}

# Connection to the database
try:
    conn = mariadb.connect(**config)
    cursor = conn.cursor()

    # Define a list of table names to check and create
    table_names = ['users']

    # Loop through the table names and check if each table exists
    for table_name in table_names:
        cursor.execute("SHOW TABLES LIKE %s", (table_name,))
        result = cursor.fetchone()

        # If the table doesn't exist, create it
        if not result:
            cursor.execute(f"CREATE TABLE {table_name} (id INT PRIMARY KEY, username VARCHAR(255), password VARCHAR(255))")
            conn.commit()

except mariadb.Error as e:
    print(f"Error connecting to MariaDB: {e}")
    sys.exit(1)



# Login route
@app.route('/login', methods=['POST'])
def login():
    # Get username and password from the request
    username = request.json['username']
    password = request.json['password'].encode('utf-8')
    
    # Get hashed password from the database
    cursor.execute("SELECT password FROM users WHERE username=?", (username,))
    hashed_password = cursor.fetchone()[0].encode('utf-8')
    
    # Check if the password is correct
    if bcrypt.checkpw(password, hashed_password):
        return jsonify({'success': True})
    else:
        return jsonify({'success': False})

# Signup route
@app.route('/signup', methods=['POST'])
def signup():
    # Get username and password from the request
    username = request.json['username']
    password = request.json['password'].encode('utf-8')
    
    # Hash the password
    hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
    
    # Insert the user into the database
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
        conn.commit()
        return jsonify({'success': True})
    except mariadb.Error as e:
        print(f"Error inserting user into database: {e}")
        conn.rollback()
        return jsonify({'success': False})

# Run the app
if __name__ == '__main__':
    app.run()