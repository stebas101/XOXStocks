import csv, os

from flask import current_app

from app import db
from app import models as m


data_path = os.path.join(current_app.instance_path, 'data/')
symbols_file = 'symbols.csv'

def fill_data():
    file = data_path + symbols_file
    print(f'Reading {file}')
    with open(file, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            print(row['symbol'], row['short_name'])
            s = m.Symbol(symbol=row['symbol'], short_name=row['short_name'])
            db.session.add(s)
    db.session.commit()