import csv
import sqlite3


db_file = 'instance/xoxstocks.sqlite'
db = sqlite3.connect(db_file, detect_types=sqlite3.PARSE_DECLTYPES)

file = 'xoxstocks/data/symbols.csv'
with open(file, newline='') as f:
    reader = csv.DictReader(f)
    # reader = csv.reader(f, delimiter=',')
    for row in reader:
        # print(row['symbol'], row['short_name'])
        # print(row)
        db.execute(
            "INSERT INTO asset (symbol, short_name) VALUES (?, ?)",
            (row['symbol'], row['short_name']),
        )
        
db.commit()