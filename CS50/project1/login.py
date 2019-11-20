# -*- coding: utf-8 -*-
"""
Created on Mon Jan 21 20:05:07 2019
Login and Logout function

@author: ddeen
"""

# %% import
from flask import Blueprint, request, session, flash, url_for, redirect, render_template
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

from DBconnection import DBconnection

# Blueprint
login_flask = Blueprint('login_flask', __name__, template_folder='templates')

# Set up database
db = DBconnection()


# %% Function and pages
def loginRequired(f):
    '''
    Check if the user is logged in:
        - if YES: allow access to the page
        - if NOT: redirect to login page
    '''
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login first!')
            return redirect(url_for('login_flask.login'))
    return wrap


@login_flask.route('/login', methods=['GET','POST'])
def login():
    '''
    Login:
        - GET: show login page
        - POST: Verify login user and password
    '''
    if request.method == 'POST':
        # Check username existence
        user_presence = db.execute('SELECT count(*) AS N FROM users WHERE username = :username', 
                              {'username':request.form['username']}).fetchone()
        if user_presence[0] == 0:
            flash('User not registered!')
            return render_template('register.html')
        
        # Check password
        password = db.execute("SELECT password FROM users WHERE username = :username",
                              {'username':request.form['username']}).fetchone()
        if check_password_hash(password[0], request.form['password']):
            session['logged_in'] = True
        else:
            flash('wrong password!')
            return render_template('login.html')
        
        return redirect(url_for('index'))
    
    elif request.method == 'GET':
        return render_template('login.html')        # Login page

    
@login_flask.route("/logout")
def logout():
    '''
    Logout
    '''
    session.pop('logged_in', None)
    return redirect(url_for('index'))               # return to index page
