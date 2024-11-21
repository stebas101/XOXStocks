import os
import click
import csv

from flask import Blueprint, current_app
import sqlalchemy as sa

from app import db
from app.models import Symbol


bp = Blueprint('cli', __name__, cli_group=None)


@bp.cli.group()
def symb():
    """Symbol table management commands."""
    pass


@symb.command()
@click.argument('symb_file')
def load(symb_file):
    """Populates the symbols table using a csv file.
    If a symbol already exists in the table, its data will be updated.
    """
    # path = current_app.config['SYMBOL_DATA_PATH']
    # symb_file = os.path.join(path, symb_file)
    with open(symb_file, 'r') as f:
        reader = csv.DictReader(f)
        added = 0
        updated = 0
        for row in reader:
            symb = Symbol(symbol=row['symbol'], name=row['name'])
            symb_db = db.session.scalar(sa.select(Symbol).where(
            Symbol.symbol == symb.symbol))
            
            if symb_db is None:
                db.session.add(symb)
                print('Adding: ', symb)
                added += 1
            else:
                symb_db.update(symb)
                print('Updating: ', symb_db)
                updated += 1
            
        db.session.commit()
        print(f'{added} symbols added.\n{updated} symbols updated.')
        

@symb.command()
def list():
    """Lists available files in the default data path."""
    path = current_app.config['SYMBOL_DATA_PATH']
    files = os.listdir(path)
    print(f'Files in {path}:')
    for f in files:
        print(f'- {f}')
        
        
@symb.command()
@click.argument('symb_file')
def check_file(symb_file):
    """Checks if the data file contains the required fields."""
    # TODO check the header contains the correct field names
    # DictReader.fieldnames
    # DictReader.dialect == 'excel'
    # DictReader.line_num > 1
    # no None values
    raise NotImplementedError