# Project 2

Web Programming with Python and JavaScript
https://docs.cs50.net/web/2019/x/projects/2/project2.html
Development of the project: main focus on the functionality than on style and responsiveness.


## Problem
There are some problem with debug and socket (https://stackoverflow.com/questions/53522052/flask-app-valueerror-signal-only-works-in-main-thread)
The debug is not working: run the following command
flask run --no-reload


## Description
The project follows the indication of Requirements, and it's a 2 page application, one for login and the other for all channels and messages;
A personal touch is the possibility to delete own messages, and the possibility to use Enter instead of clicking on buttons.

All Server side operation are in the "application.py" script:
- login and home pages;
- API for requesting and pushing channel, user, messages;
- Emit to broadcast info to all clients;

All other functionality are managed by javascript:
- login.js for login operation
- index.js for creating channels and messages, waiting for broadcast from server, etc.