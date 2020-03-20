# Project 3

Web Programming with Python and JavaScript

## Install
- Install Docker
- Run (in the main folder) `docker-compose build` and then `docker-compose up` (the command `python manage.py runserver` is inside the docker-compose commands)
- Access to the shell inside docker: `docker exec -it container_name /bin/bash`
- Run `python manage.py makemigrations` (this is always manual, to let the user know something changed) and then `python mangage.py migrate` (this has been add to docker-compose), the first time, and every time there has been a change in code to `models.py`

- To access the shell: `python manage.py shell`
- To create admin: `python manage.py createsuperuser`


## Import data
Data are imported from "http://www.pinocchiospizza.net/menu.html" through /fextures/data.json file
Launch the command `python manage.py loaddata data.json`
(https://docs.djangoproject.com/en/3.0/howto/initial-data/)


## Configuration
- Have docker installed
- Have the following ENV variable in sysmet (they are taken by docker)
```
SET EMAIL_HOST=smtp.gmail.com
SET EMAIL_PORT=587
SET EMAIL_HOST_USER=myemail
SET EMAIL_HOST_PASSWORD=pass
```

## Program
- Launch start.bat