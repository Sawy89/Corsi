'''
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
db_version = 'v1'


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



# %% Main
if __name__ == "__main__":
    db = DBconnection()

