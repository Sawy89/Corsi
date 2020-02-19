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
message_id = [0] # for counting messages, and identify univoquely


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
                    'insertdate': datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')}]}
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


# %% API messages
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
    message_id[0] += 1

    # Extract data
    channel = data['channel']
    new_message = { 'channel': channel,
                    'id': "mesid-"+str(message_id[0]),
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


@app.route("/channel/delmessage", methods=['POST'])
def del_message():
    '''
    Delete a message, only if sent from the same username that is deleting (check by frontend)
    JSON: channel, username, message, insertdate
    '''
    print(request.json)
    if request.json and 'channel' in request.json and 'username' in request.json \
             and 'message' in request.json  and 'insertdate' in request.json:
        # message to delete
        message_to_del = request.json
        # Search for the channel
        flag_channel_found = False
        for channel_dict in channels:
            if channel_dict['name'] == request.json['channel']:
                flag_channel_found = True
                # Search for the message
                if message_to_del in channel_dict['messages']:
                    # delete the message and emit
                    channel_dict['messages'].remove(message_to_del)
                    socketio.emit("message deleted to client", message_to_del, broadcast=True)
                    return jsonify({"text": "Message deleted!"}), 200
                else:
                    return jsonify({"error": "Message not found"}), 404
        return jsonify({"error": "Channel not found"}), 404
    else:
        return jsonify({"error": "Method not supported or wrong parameters."}), 405
    