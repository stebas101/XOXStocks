# XOXStocks
## A stock and ETF screener based on Flask
#### Video Demo:  <URL HERE>

TODO
- what my project does
- what each of the files contains and does
- design choices: why

### Installation

### Project description:

#### Design and Components
- use of WTForms and FlaskWTForms allows to streamline the form validation and to implement CSRF key encription on form data

- use of SQLAlchemy: ORM approach, replacing sqlite with MySQL or PostgreSQL

- AJAX

- styled using Bootstrap

#### File structure

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
