-- Script for creating the DB schema!


-- drop tables
DROP TABLE IF EXISTS reviews;
DROP TABLE IF EXISTS books;
DROP TABLE IF EXISTS users;

-- TABLE USER
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR NOT NULL,
    password VARCHAR NOT NULL,
    insertdate TIMESTAMP NOT NULL
);


-- TABLE BOOKS
CREATE TABLE books (
    book_id SERIAL PRIMARY KEY,
    isbn CHAR(13) UNIQUE NOT NULL,
    title VARCHAR NOT NULL,
    author VARCHAR NOT NULL,
    year INTEGER NOT NULL,
    insertdate TIMESTAMP NOT NULL
);


-- TABLE REVIEW
CREATE TABLE reviews (
    review_id SERIAL PRIMARY KEY,
    rating INTEGER NOT NULL,
    opinion VARCHAR,
    book_id INTEGER NOT NULL REFERENCES books,
    user_id INTEGER NOT NULL REFERENCES users,
    insertdate TIMESTAMP NOT NULL
);