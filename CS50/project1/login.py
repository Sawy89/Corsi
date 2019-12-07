# -*- coding: utf-8 -*-
"""
Created on Mon Jan 21 20:05:07 2019
Login and Logout function

@author: Sawy89
"""

# %% import
from flask import Blueprint, request, session, flash, url_for, redirect, render_template
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import datetime

from models import *

# Blueprint
login_flask = Blueprint('login_flask', __name__, template_folder='templates')


# %% Function and pages
def loginRequired(f):
    '''
    Check if the user is logged in:
        - if YES: allow access to the page
        - if NOT: redirect to login page
    '''
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'user_id' in session:
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
        user_presence = User.query.filter_by(username=request.form['username']).count()
        if user_presence == 0:
            flash('User not registered!')
            return render_template('register.html')
        
        # Check password
        password = User.query.with_entities(User.password).filter_by(username=request.form['username']).first()
        if check_password_hash(password[0], request.form['password']):
            user_id = User.query.with_entities(User.user_id).filter_by(username=request.form['username']).first()
            session['user_id'] = user_id[0]
        else:
            flash('wrong password!')
            return render_template('login.html')
        
        return redirect(url_for('index'))
    
    elif request.method == 'GET':
        return render_template('login.html')        # Login page


@login_flask.route('/register', methods=['GET','POST'])
def register():
    '''
    Register an account:
        - POST: save new account on DB
        - GET: insert data of the new account
    '''
    if request.method == 'POST':
        # insert new account on DB
        user_presence = User.query.filter_by(username=request.form['username']).count()
        if user_presence == 0:
            # Insert
            adesso = datetime.datetime.now()
            user = User(username=request.form['username'], password=generate_password_hash(request.form['password']), insertdate=adesso)
            db.session.add(user)
            db.session.commit()
            flash('User '+request.form['username']+' correctly registered! Thank you!')
        else:
            flash('Username already registered; please chose another username!')
            return render_template('register.html')
     
        return redirect(url_for('login_flask.login'))
    
    elif request.method == 'GET':
        return render_template('register.html')        # Register form

    
@login_flask.route("/logout")
def logout():
    '''
    Logout
    '''
    session.pop('user_id', None)
    return redirect(url_for('index'))               # return to index page
