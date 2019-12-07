# -*- coding: utf-8 -*-
"""
Created on Sat Nov 16 15:51:32 2019

Main of the FLASK application fo book review site:
- register, login and logout
- search for book in the database by Title, ISBN, author
- visualize some info on selected book, visualize review, add review
- access some info through API

@author: Sawy89
"""

# %% Import
from flask import Flask, render_template, redirect, url_for, request, flash, session, jsonify, abort
from flask_session import Session
import datetime

from DBconnection import DBconnection, APIgoodreader_getreview
from login import login_flask, loginRequired
from models import *
from sqlalchemy import and_
from sqlalchemy.sql import func


# %% MAIN
app = Flask(__name__)

# Blueprint
app.register_blueprint(login_flask, url_prefix='/auth')


# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["SQLALCHEMY_DATABASE_URI"] = DBconnection(get_uri=True)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
Session(app)

# Link the Flask app with the database (no Flask app is actually being run yet).
db.init_app(app)


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
        books = Book.query.filter(and_(Book.isbn.ilike("%"+request.form['isbn']+"%"), 
                                        Book.title.ilike("%"+request.form['title']+"%"),
                                        Book.author.ilike("%"+request.form['author']+"%"))).all()
        input_form = request.form
    else:
        books = None
        input_form = None

    return render_template('search.html', books=books, input_form=input_form)


@app.route("/books/<int:book_id>")
@loginRequired
def book(book_id):
    '''
    display a specific book with all his information
    '''

    # Make sure the book exists.
    book = Book.query.filter_by(book_id=book_id).first()
    if book is None:
        flash("The book selected doesn't exist")
        return render_template("index.html")

    # Get all review.
    reviews = Review.query.filter_by(book_id=book_id).all()
    
    # Get data from GoodReader!
    grapi = APIgoodreader_getreview(book.isbn)
    
    # Add review only if there are no review from the user
    # add_review = False if session['user_id'] in [review.user_id for review in reviews] else True
    if session['user_id'] in [review.user_id for review in reviews]:
        add_review = False
    else:
        add_review = True

    return render_template("book.html", book=book, reviews=reviews, add_review=add_review, grapi=grapi)


@app.route("/api/<isbn>")
def api(isbn):
    '''
    API for getting book data
    '''

    # Make sure the book exists.
    book = Book.query.filter_by(isbn=isbn).first()
    if book is None:
        return jsonify({"error": "ISBN not found"}), 404

    # Get all review.
    reviews = Review.query.with_entities(func.count(Review.rating).label('n_review'),
                                func.avg(Review.rating).label('avg_rating')).filter_by(book_id=book.book_id).first()
    
    # Get data from GoodReader!
    grapi = APIgoodreader_getreview(book.isbn)

    # creo dizionario
    diz_json = {"title": book.title, "author": book.author, "year": book.year, 
            "isbn": book.isbn, "review_count": reviews.n_review, "average_score": str(reviews.avg_rating),
            "goodread_review_count": grapi['work_ratings_count'], "goodread_average_score": grapi['average_rating']}

    return jsonify(diz_json)


@app.route("/books/insert", methods=['POST'])
@loginRequired
def review_insert():
    '''
    Insert a new review on database
    '''
    # Get form information.
    opinion = request.form.get("opinion")
    try:
        rating = int(request.form.get("rating"))
    except ValueError:
        flash('Invalid rating inserted!')
        return render_template("index.html")
    try:
        book_id = int(request.form.get("book_id"))
    except ValueError:
        flash('Invalid book_id!')
        return render_template("index.html")
    adesso = datetime.datetime.now()
    user_id = session['user_id']
    
    # Make sure the book exists.
    book = Book.query.filter_by(book_id=book_id).first()
    if book is None:
        flash("The book selected doesn't exist")
        return render_template("index.html")
    
    # Insert the review
    review = Review(rating=rating, opinion=opinion, book_id=book_id,
                        user_id=user_id, insertdate=adesso)
    db.session.add(review)
    db.session.commit()

    flash("Review inserted with success!")
    return redirect(url_for('book', book_id=book_id))


