'''
Connection to DB:
- Read a txt file containing info for connecting to DB
- open the connection to DB

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


def DBconnection():
    '''
    Create a connection to DB
    '''
    # Get config
    d = readConfig()
    
    engine = create_engine(d['DB_URI'])
    db = scoped_session(sessionmaker(bind=engine))
    
    return db



# %% Main
if __name__ == "__main__":
    db = DBconnection()

