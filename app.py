from flask import Flask, request, jsonify, render_template, redirect, url_for
import json

app = Flask(__name__)

# Load data from JSON file
def load_data():
    with open('data.json', 'r') as file:
        return json.load(file)

# Save data to JSON file
def save_data(data):
    with open('data.json', 'w') as file:
        json.dump(data, file, indent=4)

# Home route
@app.route('/')
def home():
    return render_template('index.html')

# User registration route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        data = load_data()
        # Check if user already exists
        if any(user['username'] == username for user in data['users']):
            return 'Kullanıcı zaten mevcut!'
        # Add new user
        data['users'].append({'username': username, 'password': password})
        save_data(data)
        return redirect(url_for('login'))
    return render_template('register.html')

# User login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        data = load_data()
        # Authenticate user
        if any(user['username'] == username and user['password'] == password for user in data['users']):
            return redirect(url_for('dashboard'))
        return 'Geçersiz kullanıcı adı veya şifre!'
    return render_template('login.html')

# Add a new post
@app.route('/add_post', methods=['GET', 'POST'])
def add_post():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        date = request.form['date']
        platform = request.form['platform']
        data = load_data()
        data['posts'].append({
            'title': title,
            'description': description,
            'date': date,
            'platform': platform
        })
        save_data(data)
        return redirect(url_for('view_posts'))
    return render_template('add_post.html')

# View posts
@app.route('/view_posts')
def view_posts():
    data = load_data()
    return render_template('view_posts.html', posts=data['posts'])

# Dashboard route
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

# Logout route
@app.route('/logout')
def logout():
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True) 