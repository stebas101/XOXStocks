# XOXStocks
## A Stock and ETF screener based on Flask
#### Video Demo:  <URL HERE>
#### Description:

__Note: project still in progress__

__XOXStocks__ is a self-contained Stock and ETF screener web application based on Flask. I developed it as a final project for the [CS50's _Introduction to Computer Science_](https://cs50.harvard.edu/x/2024) course.

#### Disclaimer

educational purposes

no guarantee about the accuracy of the data provided by the app

it shouldn't be used to make investment decisions

### Project description:

TODO

#### How to install and run

TODO

#### Design and Components

TODO

- use of WTForms and FlaskWTForms allows to streamline the form validation and to implement CSRF key encription on form data

- use of SQLAlchemy: ORM approach, replacing sqlite with MySQL or PostgreSQL

- use of database migrations

- AJAX

- styled using Bootstrap

- tests - unittest

- race conditions ?

#### File structure

TODO

```
.
├── README.md
├── app
│   ├── __init__.py
│   ├── api.py
│   ├── auth.py
│   ├── fill_data.py
│   ├── forms.py
│   ├── models.py
│   ├── routes.py
│   ├── static
│   │   └── style.css
│   └── templates
│       ├── _formhelpers.html
│       ├── auth
│       │   ├── login.html
│       │   └── register.html
│       ├── index.html
│       ├── layout.html
│       └── watchlist.html
├── config.py
├── instance
│   ├── data
│   │   └── symbols.csv
│   └── database.db
├── migrations
│   ├── README
│   ├── alembic.ini
│   ├── env.py
│   ├── script.py.mako
│   └── versions
│       └── 4f52b126910e_users_table.py
├── pyproject.toml
├── tests
├── tests.py
└── xoxstocks.py
```

#### Nice to add

- Email confirmation upon registration
- Email token to reset password
- race conditions to help use with several concurrent users

### Sources and References

[1][The tutorial](https://flask.palletsprojects.com/en/3.0.x/tutorial/) in the Flask official documentation.

[2][Flask-SQLAlchemy Tutorial](https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/quickstart/)

[3][Flask _mega tutorial_](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iv-database) by Miguel Grinberg

[4][Digital Ocean blog: How to use Flask-SQLAlchemy to interact with databases in a Flask application](https://www.digitalocean.com/community/tutorials/how-to-use-flask-sqlalchemy-to-interact-with-databases-in-a-flask-application)

[5][Digital Ocean blog: how to query tables and paginate data in Flask-SQLAlchemy](https://www.digitalocean.com/community/tutorials/how-to-query-tables-and-paginate-data-in-flask-sqlalchemy)