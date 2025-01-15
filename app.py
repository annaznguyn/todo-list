from flask import Flask, render_template, request, url_for, abort
from flask_socketio import SocketIO
import json
import bcrypt

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template("login.html")

@app.route('/signup')
def signup():
    return render_template("signup.html")

# Handle post request from login page, send back a URL to home page
@app.route('/login/user', methods=['POST'])
def handle_login():
    if not request.is_json:
        abort(404)

    username = request.json.get("username")
    password = request.json.get("password")

    try:
        with open("data.json", "r") as f:
            data = json.load(f)
            if username in data:
                # hash the input password and compare it with the hash value stored in the json file
                salt = data[username]["salt"].encode('utf-8')
                hash = bcrypt.hashpw(password.encode('utf-8'), salt)
                
                stored_hash = data[username]["password"].encode('utf-8')
                if hash == stored_hash:
                    return url_for("home", username=username)
                else:
                    return "Password doesn't match"
            else:
                return "Username doesn't exist"
    except FileNotFoundError:
        return "json file not found"

    return "Unexpected error"

@app.route('/signup/user', methods=['POST'])
def handle_signup():
    if not request.is_json:
        abort(404)

    username = request.json.get("username")
    password = request.json.get("password")

    try:
        with open("data.json", "r") as f:
            data = json.load(f)

            if username in data:
                return "Username already exists"
        
        with open("data.json", "w") as f:
            salt = bcrypt.gensalt()
            hash = bcrypt.hashpw(password.encode('utf-8'), salt)
            data[username] = {
                "password": hash.decode('utf-8'),
                "salt": salt.decode('utf-8'),
                "todo-items": []
            }

            json.dump(data, f, indent=4)
    except FileNotFoundError:
        return "json file not found"

    return url_for("home", username=username)

@app.route('/home/add-item', methods=['POST'])
def add_item():
    if not request.is_json:
        abort(404)

    username = request.json.get("username")
    todo_item = request.json.get("content")

    try:
        with open("data.json", "r") as f:
            data = json.load(f)

            new_data = {
                "content": todo_item,
                "status": "incomplete"
            }
        
            data[username]["todo-items"].append(new_data)

        with open("data.json", "w") as f:
            json.dump(data, f, indent=4)

    except FileNotFoundError:
        return "json file not found"

    return url_for("home")

@app.route('/home')
def home():
    username = request.args.get("username")

    try:
        with open("data.json", "r") as f:
            data = json.load(f)
            todo_items = data[username]["todo-items"]
    except FileNotFoundError:
        return "json file not found"

    return render_template("home.html", username=username, todo_items=json.dumps(todo_items))

if __name__ == "__main__":
    socketio.run(app, debug=True)