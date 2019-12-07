# -*- coding: utf-8 -*-
"""
Created on Thu Dec 05 20:50:32 2019

DB class for ORM

@author: Sawy89
"""

# %% import & init
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# %% DB model
class User(db.Model):
    '''
    Table with the list of registered users
    '''
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    insertdate = db.Column(db.TIMESTAMP, nullable=False)

    def __init__(self, username, password, insertdate):
        self.username = username
        self.password = password
        self.insertdate = insertdate

class Book(db.Model):
    '''
    Table with the list of books
    '''
    __tablename__ = 'books'

    book_id = db.Column(db.Integer, primary_key=True)
    isbn = db.Column(db.String(13), nullable=False, unique=True)
    title = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    insertdate = db.Column(db.TIMESTAMP, nullable=False)


class Review(db.Model):
    '''
    Table with the list of books
    '''
    __tablename__ = 'reviews'

    review_id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    opinion = db.Column(db.String)
    book_id = db.Column(db.Integer, db.ForeignKey("books.book_id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    insertdate = db.Column(db.TIMESTAMP, nullable=False)

    def __init__(self, rating, opinion, book_id, user_id, insertdate):
        self.rating = rating
        self.opinion = opinion
        self.book_id = book_id
        self.user_id = user_id
        self.insertdate = insertdate
