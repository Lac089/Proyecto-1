import sqlite3
import csv

#Create Database pizza.sqlite
conn = sqlite3.connect('pizza.sqlite')
cur = conn.cursor()


# Create tables for orders, individual pizzas, recipes, types and a connection table  for ingredients
cur.executescript('''
CREATE TABLE IF NOT EXISTS Orders (
    id     INTEGER NOT NULL PRIMARY KEY UNIQUE,
    date     TIMESTAMP NOT NULL 
);


CREATE TABLE IF NOT EXISTS Pizza (
    id     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    order_id INTEGER NOT NULL,
    size TEXT(1) NOT NULL,
    recipe_id INTEGER NOT NULL,
    price INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS Type (
    id     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name  TEXT UNIQUE
);

CREATE TABLE IF NOT EXISTS Recipe (
    id     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name  TEXT UNIQUE,
    type_id INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS Ingredient (
    id     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name  TEXT UNIQUE
);

CREATE TABLE IF NOT EXISTS Connection (
    recipe_id INTEGER NOT NULL,
    ingr_id INTEGER NOT NULL,
    PRIMARY KEY (recipe_id,ingr_id)
)

''')

#Open file daa.csv
file = open('data.csv')
reader = csv.reader(file)

rows = []
for row in reader:
        rows.append(row)
#['49569', '2015-021347', '12/31/2015', '21:14:37', 'peppr_salami', 'S', 'supreme', '12.5']

def real_Date(date,time):
        pos = date.find('/')
        year = date[-4:]
        day = date[pos+1:pos+3]
        if day[1] == '/':
                day = '0' + day[0]
        month = date[:pos]
        if len(month) == 1:
                month = '0' + month
        real = year + '-' + month + '-' + day + ' ' + time
        return real


for row in rows:
        pos = row[1].find('-')
        order_id = int(row[1][pos+1:])
        date = real_Date(row[1],row[2])
        size = row[5]
        recipe = row[4]
        price = row[7]
        type = row[6]

        cur.execute('''INSERT OR IGNORE INTO Type (name)
        VALUES ( ? )''', ( type, ) )
        cur.execute('SELECT id FROM Type WHERE name = ? ', (type, ))
        type_id = cur.fetchone()[0]
        
        cur.execute('''INSERT OR IGNORE INTO Recipe (name, type_id)
        VALUES ( ? , ? )''', ( recipe, type_id ) )
        cur.execute('SELECT id FROM Recipe WHERE name = ? ', (recipe, ))
        recipe_id = cur.fetchone()[0]

        cur.execute('''INSERT OR IGNORE INTO Orders (id, date)
        VALUES ( ? , ? )''', ( order_id, date ) )

        cur.execute('''INSERT OR IGNORE INTO Pizza (order_id, size, recipe_id, price )
        VALUES ( ? , ?, ?, ?)''', ( order_id, size, recipe_id, price ))
           
conn.commit()

fhand =open('ingredients.txt')


for line in fhand:
    if len(line) == 1:
        continue
    pos = line.find(':')
    recipe = line[:pos]
    cur.execute('SELECT id FROM Recipe WHERE name = ? ', (recipe, ))
    recipe_id = int(cur.fetchone()[0])
    ingredients = line[pos+2:].split(", ")
    for ing in ingredients:
        cur.execute('''INSERT OR IGNORE INTO Ingredient (name)
        VALUES ( ? )''', ( ing, ) )
        cur.execute('SELECT id FROM Ingredient WHERE name = ? ', (ing, ))
        ing_id = int(cur.fetchone()[0])
        cur.execute('''INSERT OR IGNORE INTO Connection (recipe_id, ingr_id)
        VALUES ( ?,? )''', ( ing_id, recipe_id) )
conn.commit()
      