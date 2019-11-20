import os

from flask import Flask
from flask_session import Session
# from sqlalchemy.orm import scoped_session, sessionmaker
from DBconnection import DBconnection

app = Flask(__name__)

# Check for environment variable


# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
db = DBconnection()


@app.route("/")
def index():
    return "Project 1: TODO prova"
