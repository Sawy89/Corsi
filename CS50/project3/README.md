# Project 3

Web Programming with Python and JavaScript

## Install
- Install Docker
- Run (in the main folder) `docker-compose build` and then `docker-compose up` (the command `python manage.py runserver` is inside the docker-compose commands)
--> you can do it easily by running the file `start.bat`
- Access to the shell inside docker: `docker exec -it container_name /bin/bash`
- Run `python manage.py makemigrations` (this is always manual, to let the user know something changed) and then `python mangage.py migrate` (this has been add to docker-compose), the first time, and every time there has been a change in code to `models.py`

- To access the shell: `python manage.py shell`
- To create admin: `python manage.py createsuperuser`


## Import data
Data are imported from "http://www.pinocchiospizza.net/menu.html" through /fextures/data.json file
Launch the command `python manage.py loaddata data.json`
(https://docs.djangoproject.com/en/3.0/howto/initial-data/)


## Configuration & Launch program
- Have the following ENV variable in system (they are taken by docker)
    ```
    SET EMAIL_HOST=smtp.gmail.com
    SET EMAIL_PORT=587
    SET EMAIL_HOST_USER=myemail
    SET EMAIL_HOST_PASSWORD=pass
    ```
- Launch start.bat


## Program description
The project is solved with django and javascript.
The project respect requirements, with some add on:
- reset password by mail
- order page where users can see their pending and completed orders
- confirmation mail when an order is completed
The project is structured with

### File description
- static file: in `cart.js`, `menu.js` and `base.js` there is some javascript code for performing some action, mainly related to the menu display and cart management 
- templates: `base.html` and `index.html` are the common layout and the home page; then in `registration\*.html` there are pages that overwrites base django registration templates; `menu.html` lists the menu, `cart.html` is the page for the shopping cart of the user and `orders.html` lists the pending and completed orders for the user; for Admin default pages has been used
- `models.py` contains all DB models, with some functions (for easily display data, and for sending order mail)
- `views.py` contains all pages of the project
- `forms.py` contains the form for user registration modified for respect req
- `admin.py` contains some modification to default for modifying the menu and view and complete orders
