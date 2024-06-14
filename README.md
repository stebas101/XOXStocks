# XOXStocks
## A Stock and ETF screener based on Flask
#### Video Demo:  <URL HERE>

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

- AJAX

- styled using Bootstrap

- tests

#### File structure

TODO

```
.
├── README.md
├── instance
│   └── xoxstocks.sqlite
├── populate.py
├── pyproject.toml
├── tests
└── xoxstocks
    ├── __init__.py
    ├── api.py
    ├── auth.py
    ├── data
    │   └── symbols.csv
    ├── db.py
    ├── forms.py
    ├── models.py
    ├── routes.py
    ├── schema.sql
    ├── static
    │   └── style.css
    └── templates
        ├── _formhelpers.html
        ├── auth
        │   ├── login.html
        │   └── register.html
        ├── index.html
        ├── layout.html
        └── watchlist.html
```

#### Nice to add

- Database migrations

### Sources

TODO

[digital ocean blog](https://www.digitalocean.com/community/tutorials/how-to-use-flask-sqlalchemy-to-interact-with-databases-in-a-flask-application)

Miguel Grinberg's [Flask _mega tutorial_](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iv-database)

Flask tutorial

https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/quickstart/

https://www.digitalocean.com/community/tutorials/how-to-query-tables-and-paginate-data-in-flask-sqlalchemy