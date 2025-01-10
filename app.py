from flask import Flask, render_template, request, url_for, abort
from flask_socketio import SocketIO
import pickle
import json

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

    with open("data.json", "r") as f:
        data = json.load(f)
        if username in data:
            stored_pwd = data[username]["password"]
            if stored_pwd == password:
                return url_for("home")
            else:
                return "Password doesn't match"
        else:
            return "Username doesn't exist"

    return "Unexpected error"

@app.route('/signup/user', methods=['POST'])
def handle_signup():
    if not request.is_json:
        abort(404)

    username = request.json.get("username")
    password = request.json.get("password")

    with open("data.json", "r") as f:
        data = json.load(f)

        if username in data:
            return "Username already exists"
    
    # TODO: hash pwd
    with open("data.json", "w") as f:
        data[username] = {
            "password": password
        }

        json.dump(data, f, indent=4)

    return url_for("home")

@app.route('/home')
def home():
    return render_template("home.html")

if __name__ == "__main__":
    socketio.run(app, debug=True)