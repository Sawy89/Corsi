import os

from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)


# %% Variables
usernames = []  # for storing registered user
channels = []


# %% Pages
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login")
def login():
    return render_template("login.html")


# %% API
@app.route("/register/check/<username>", methods=['GET'])
def register_check(username):
    '''
    Check if the requested user was already logged;
    '''
    already_registered = True if username in usernames else False
    return jsonify({"registered": already_registered}), 200


@app.route("/register/new", methods=['POST'])
def register_new():
    '''
    Check if the requested user was already logged;
     if not, it saves it!
    '''
    if request.json and 'username' in request.json and 'already_registered' in request.json:
        username = request.json['username']
        already_registered = request.json['already_registered']
    else:
        return jsonify({"registered": False, "error": "Method not supported"}), 405
    
    if already_registered == True and username in usernames:
        return jsonify({"registered": True}), 200
    elif already_registered == False and username in usernames:
        return jsonify({"registered": False, "error": "Username already used"}), 409
    else:
        usernames.append(username)
        return jsonify({"registered": True}), 200



