import sqlite3
import csv

def list_rows(path):
    """return a file as a list of rows

    Keyword arguments:
    path: The path of the file to open
    """
    with open(path) as file: 
        reader = csv.reader(file) 
        rows = []
        for row in reader:
            rows.append(row)
        del rows[0]
        return rows

def real_Date(date,time):
    """Receive a date in format 'mm/dd/yyyy' and a time and return a TIMESTAMP in format 'yyy-mm-dd hh:mm:ss'

    Keyword arguments:
    date: String date in mm/dd/yyyy format
    time: String time in hh:mm:ss
    """
    
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

def ins_type(type):
    """Insert each unique type in the Type Table"""
    cur.execute('''INSERT OR IGNORE INTO Type (name) VALUES ( ? )''', ( type, ) )
    cur.execute('SELECT id FROM Type WHERE name = ? ', (type, ))
    return cur.fetchone()[0]
    
def ins_recipe(recipe, type_id ):
    """Insert each unique recipe in the Recipe Table"""
    cur.execute('''INSERT OR IGNORE INTO Recipe (name, type_id) VALUES ( ? , ? )''', ( recipe, type_id ) )
    cur.execute('SELECT id FROM Recipe WHERE name = ? ', (recipe, ))
    return cur.fetchone()[0]

def ins_orders( order_id, date ):
    """Insert each unique order in the Order Table"""
    cur.execute('''INSERT OR IGNORE INTO Orders (id, date) VALUES ( ? , ? )''', ( order_id, date ) )

def ins_pizza(order_id, size, recipe_id, price ):
    """Insert each unique pizza in the Pizza Table"""
    cur.execute('''INSERT OR IGNORE INTO Pizza (order_id, size, recipe_id, price ) VALUES ( ? , ?, ?, ?)''', ( order_id, size, recipe_id, price ))

def insert_ing(ing,recipe_id):
    """Insert each unique ingredient in the ingredient Table"""
    cur.execute('''INSERT OR IGNORE INTO Ingredient (name) VALUES ( ? )''', ( ing, ) )
    cur.execute('SELECT id FROM Ingredient WHERE name = ? ', (ing, ))
    ing_id = int(cur.fetchone()[0])
    cur.execute('''INSERT OR IGNORE INTO Connection (recipe_id, ingr_id) VALUES ( ?,? )''', ( ing_id, recipe_id) )


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

#Open file data.csv and create the list of rows
rows =list_rows('data.csv')

#extract the orderid, date, size, recipe, price, and type of the pizza and insert them in the database
for row in rows:
        pos = row[1].find('-')
        order_id = int(row[1][pos+1:])
        date = real_Date(row[1],row[2])
        size = row[5]
        recipe = row[4]
        price = row[7]
        type = row[6]

        type_id = ins_type(type)
        recipe_id = ins_recipe(recipe, type_id )
        ins_orders( order_id, date )
        ins_pizza(order_id, size, recipe_id, price )
                
conn.commit()

with open('ingredients.txt') as filehandle: 
#read the file ingredients.txt and insert each ingredient in the database
    for line in filehandle:
        if len(line) == 1:
            continue
        pos = line.find(':')
        recipe = line[:pos]
        cur.execute('SELECT id FROM Recipe WHERE name = ? ', (recipe, ))
        recipe_id = int(cur.fetchone()[0])
        ingredients = line[pos+2:].split(", ")
        for ing in ingredients:
            insert_ing(ing,recipe_id)
    conn.commit()
      