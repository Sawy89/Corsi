'''
1) Create the DB schema
2) Import file on DB

INPUT:
    - "create_schema.sql" file (in GIT) with the DB schema to be created
    - "books.csv" (not tracked) with [isbn, title, author, year] column to be uploaded
Author: Sawy89
'''


# %% import Libraries
from DBconnection import DBconnection
import csv
import datetime


# %% Read CSV
def main():
    # Read schema
    with open("create_schema.sql") as f:
        sql_schema = f.read()
    
    # Opend DB and create schema
    print('Launch SQL script for creating the schema')
    db = DBconnection()
    db.execute(sql_schema)
    print('SQL Schema created!')
    
    
    # Read CSV
    print('Load books to SQL database')
    f = open("books.csv")
    reader = csv.reader(f)
    # skip header
    r = next(reader, None)
    if r != ['isbn', 'title', 'author', 'year']:
        reader.seek(0)   # if there is no header, come back
    
    # Upload data!
    adesso = datetime.datetime.now()
    for isbn, title, author, year in reader:
        db.execute("INSERT INTO books (isbn, title, author, year, insertdate) VALUES (:isbn, :title, :author, :year, :adesso)",
                    {"isbn": isbn, "title": title, "author": author, "year": int(year), "adesso": adesso})
        # print(f"Added book '{title}' of '{author}' written in {year} [ISBN = {isbn}].")
    db.commit()
    print('BOOKS LOADED!')
    
    f.close()


# %% Main
if __name__ == "__main__":
    main()
