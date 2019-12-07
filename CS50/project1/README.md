# Project 1

Web Programming with Python and JavaScript


## SET UP ENV
You can set up the environment in two way:

1) Save those variables in a "config.txt" file that the program is going to read; below an example:
```
FLASK_APP: application.py
FLASK_ENV: development
FLASK_DEBUG: 1
DATABASE_URL: database_uri
GOODREADER_API_KEY: goodreader_api_key
```

2) Launch a config.bat file for setting all ENV variables needed (here is an example I use for debug (the database_url need the complete URL for accessing DB, with address username and password):
```
SET FLASK_APP=application.py
SET FLASK_ENV=development
SET FLASK_DEBUG=1
SET DATABASE_URL=database_uri
SET GOODREADER_API_KEY=goodreader_api_key
```

Then in the "DBconnection.py" file you have to chose the variable "db_version = 'v1'" for the approach you prefer.


## File
The project is made by the following script file:
- ```DBconnection.py``` containing the function for connecting to Database (Postgree) and taking API info from Goodreads;
- ```login.py``` with login, logout and registration function; there is also a function that is used to verify before every page that the login has been correctly done
- ```application.py``` with all other needed function for the project
- ```import.py``` and ```create_schema.sql``` for creating the Database schema and importing ```book.csv``` data in it; you only need to run ```import.py``` file to do it
- All html file in template folder

--> Upgraded for using flask_sqlalchemy as ORM for connecting to DB!

For using the API, need to pass "username" and "password" as parameters