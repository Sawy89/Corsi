import os

from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)


# %% Variables
users_name = []  # for storing registered user


# %% Pages
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login")
def login():
    return render_template("login.html")


# %% API
@app.route("/register/check/<user_name>", methods=['GET'])
def register_check(user_name):
    '''
    Check if the requested user was already logged;
    '''
    already_registered = True if user_name in users_name else False
    return jsonify({"registered": already_registered}), 200


@app.route("/register/new", methods=['POST'])
def register_new():
    '''
    Check if the requested user was already logged;
     if not, it saves it!
    '''
    if request.json and 'user_name' in request.json and 'already_registered' in request.json:
        user_name = request.json['user_name']
        already_registered = request.json['already_registered']
    else:
        print(request.json)
        return jsonify({"registered": False, "error": "Method not supported"}), 405
    
    if already_registered == True and user_name in users_name:
        return jsonify({"registered": True}), 200
    elif already_registered == False and user_name in users_name:
        return jsonify({"registered": False, "error": "Username already used"}), 409
    else:
        users_name.append(user_name)
        return jsonify({"registered": True}), 200



