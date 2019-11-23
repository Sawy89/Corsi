# -*- coding: utf-8 -*-
"""
Created on Sat Nov 16 15:51:32 2019
Try to access goodread api
Need a txt file with the key

@author: Sawy89
"""

# %% Import
from flask import Flask, render_template, redirect, url_for, request
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
    # return render_template('index.html')
    return redirect(url_for('search'))


@app.route("/search", methods=['POST','GET'])
@loginRequired
def search():
    '''
    Page for searching the book in the database
    Method:
        - GET = FORM for searching
        - POST = FORM for searching again + result
    '''
    if request.method == 'POST':
        # Query with input: download books
        books = db.execute("SELECT * FROM books WHERE LOWER(isbn) LIKE :isbn AND LOWER(title) LIKE :title AND LOWER(author) LIKE :author",
                              {'isbn':'%'+(request.form['isbn']).lower()+'%', 
                              'title':'%'+(request.form['title']).lower()+'%',
                              'author':'%'+(request.form['author']).lower()+'%'}).fetchall()
        input_form = request.form
    else:
        books = None
        input_form = None

    return render_template('search.html', books=books, input_form=input_form)
