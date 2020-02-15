import os

from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
import datetime


app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)
max_messages_per_channel = 100

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


# %% API user
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


# %% API channel
@app.route("/channel/new/<channel>", methods=['GET'])
def channel_new(channel):
    '''
    Check if a channel exist: 
    - if yes, return an error, 
    - otherwise create it and EMIT all channel
    '''
    channels_name = [i['name'] for i in channels]
    print(channels_name)
    is_new = False if channel in channels_name else True
    if is_new == False:
        return jsonify({"already_present": True}), 200
    else:
        channel_dict = {'name': channel, 'messages':[{'message': 'Channel created', 
                    'username': 'Admin',
                    'insertdate': datetime.datetime.now()}]}
        channels.append(channel_dict)
        socketio.emit("new channel", channel, broadcast=True)
        return jsonify({"already_present": False}), 200


@app.route("/channel/getall", methods=['GET'])
def channel_all():
    '''
    Return the channels list
    '''
    channels_name = [i['name'] for i in channels]
    return jsonify({"channels": channels_name}), 200


@app.route("/channel/<channel>/getmessages", methods=['GET'])
def channel_getmessages(channel):
    '''
    Return the list of messages of a specific channel
    '''
    for channel_dict in channels:
        if channel_dict['name'] == channel:
            return jsonify(channel_dict), 200
    
    return jsonify({"error": 'Channel not found!'}), 404


@socketio.on("new message to server")
def new_message(data):
    '''
    Get, save and emit a new message in a specific channel
    '''
    # Extract data
    channel = data['channel']
    new_message = { 'channel': channel,
                    'message': data['message'], 
                    'username': data['username'],
                    'insertdate': datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')}

    # save data
    flag_found = False
    for channel_dict in channels:
        if channel_dict['name'] == channel:
            flag_found = True
            channel_dict['messages'].append(new_message)    # append new message
            # delete (the first) if more than 100 messages
            if len(channel_dict['messages']) > max_messages_per_channel:
                channel_dict['messages'].pop(0)
            break   # channel found!
    if flag_found == False:
        print("Channel "+channel+" doesn't exist!")
        return jsonify({"error": 'Channel not found!'}), 404
    
    # emit the new message
    socketio.emit("new message to client", new_message, broadcast=True)