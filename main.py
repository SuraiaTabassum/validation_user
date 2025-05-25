from flask import Flask, request
import psycopg2

app = Flask(__name__)

# PostgreSQL connection
db = psycopg2.connect(
    host="dpg-d0pano3e5dus73dk7a8g-a.oregon-postgres.render.com",
    database="flask_app_6750",
    user="flask_app_6750_user",
    password="zIZIoLGRzsPYY5P4EKRHKmowP3gsDkXh",
    port=5432
)

# Create users table if not exists
def create_users_table():
    cursor = db.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(100) UNIQUE NOT NULL,
            password VARCHAR(100) NOT NULL
        );
    """)
    db.commit()
    cursor.close()

create_users_table()

@app.route('/')
def index():
    return '''
        <h2>User Login</h2>
        <form method="POST" action="/login">
            Username: <input type="text" name="username"><br><br>
            Password: <input type="password" name="password"><br><br>
            <input type="submit" value="Login">
        </form>
        <p>Don't have an account? <a href="/register">Register here</a></p>
    '''

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cursor = db.cursor()
        try:
            cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
            db.commit()
            message = '<h3>Registration successful! <a href="/">Go to Login</a></h3>'
        except psycopg2.IntegrityError:
            db.rollback()
            message = '<h3>Username already exists. Please try a different one. <a href="/register">Try again</a></h3>'
        cursor.close()
        return message
    else:
        return '''
            <h2>User Registration</h2>
            <form method="POST" action="/register">
                Username: <input type="text" name="username"><br><br>
                Password: <input type="password" name="password"><br><br>
                <input type="submit" value="Register">
            </form>
        '''

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
    user = cursor.fetchone()
    cursor.close()

    if user:
        return f"<h3>Welcome, {username}!</h3>"
    else:
        return "<h3>Invalid username or password. <a href='/'>Try again</a></h3>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
