from flask import Flask, render_template, request, url_for, abort
from flask_socketio import SocketIO

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
    print(username, password)

    return url_for("home")

@app.route('/home')
def home():
    return render_template("home.html")

if __name__ == "__main__":
    socketio.run(app, debug=True)