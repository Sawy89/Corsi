# -*- coding: utf-8 -*-
"""
Created on Sat Nov 16 15:51:32 2019
Try to access goodread api
Need a txt file with the key

@author: Sawy89
"""

# %% Import
from flask import Flask, render_template
from flask_session import Session
# from sqlalchemy.orm import scoped_session, sessionmaker

from DBconnection import DBconnection

from login import login_flask, loginRequired


# %% MAIN
app = Flask(__name__)

# Blueprint
app.register_blueprint(login_flask, url_prefix='/auth')


# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
db = DBconnection()


# %% Page
@app.route("/")
@loginRequired
def index():
    return render_template('index.html')
