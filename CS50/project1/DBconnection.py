'''
Connection to Database and API for accessing GoodReads review

V1 Connection to DB:
- Read a txt file containing info for connecting to DB
- open the connection to DB

V2 Connection to DB:
- open connection to DB from ENV variable    

Author: Sawy89
'''

# %% Read config
def readConfig():
    '''
    Read config file
    '''
    # Read KEY
    f = open("config.txt", "r")
    d = {}
    with open("config.txt") as f:
        for line in f:
            (key, val) = line.replace('\n','').split(': ')
            d[key] = val
    
    return d
    

# %% DB connection
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import os
db_version = 'v2'


def DBconnection():
    '''
    Create a connection to DB
    '''
    if db_version == 'v1':
        # Database through TXT file
        d = readConfig()    # Get config
        db_uri = d['DB_URI']

    elif db_version == 'v2':
        # Database through ENV variables
        if not os.getenv("DATABASE_URL"):
            raise RuntimeError("DATABASE_URL is not set")
        db_uri = os.getenv("DATABASE_URL")
    
    engine = create_engine(db_uri)
    db = scoped_session(sessionmaker(bind=engine))
    
    return db


# %% GoodReader API
import requests

def APIgoodreader_getreview(isbn):
    '''
    Create the connection with GoodReader API
    Get the list of books with review asked with 'isbn' input
    '''
    if db_version == 'v1':
        # API key through TXT file
        d = readConfig()    # Get config
        api_key = d['GOODREADER_API_KEY']

    elif db_version == 'v2':
        # Database through ENV variables
        if not os.getenv("GOODREADER_API_KEY"):
            raise RuntimeError("GOODREADER_API_KEY is not set")
        api_key = os.getenv("GOODREADER_API_KEY")

    # Get book data
    res = requests.get("https://www.goodreads.com/book/review_counts.json", 
        params={"key": api_key, "isbns": isbn.replace(' ','')})
    out = {}
    if res.status_code == 200:
        data = res.json()['books']
        if len(data) == 1:
            out['goodstatus'] = True
            out['work_ratings_count'] = data[0]['work_ratings_count']
            out['average_rating'] = data[0]['average_rating']
        else:
            out['goodstatus'] = False
            out['message'] = 'Too many ()'+str(len(data))+') books found!'
    elif res.status_code == 404:
        out['goodstatus'] = False
        out['message'] = 'Book not found on GoodReader!'
    else:
        out['goodstatus'] = False
        out['message'] = 'Error message '+str(res.status_code)
       
    return out




# %% Main
if __name__ == "__main__":
    db = DBconnection()

