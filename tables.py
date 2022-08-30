import sqlite3

#Create Database pizza.sqlite
conn = sqlite3.connect('pizza.sqlite')
cur = conn.cursor()


# Create tables for orders, individual pizzas, recipes, types and a connection table  for ingredients
cur.executescript('''
CREATE TABLE Orders (
    id     INTEGER NOT NULL PRIMARY KEY UNIQUE,
    date     TIMESTAMP NOT NULL 
);

CREATE TABLE Pizza (
    id     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    order_id INTEGER NOT NULL,
    size INTEGER NOT NULL,
    recipe_id INTEGER NOT NULL,
    price INTEGER NOT NULL
);

CREATE TABLE Type (
    id     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    Name  TEXT UNIQUE
);

CREATE TABLE Recipe (
    id     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name  TEXT UNIQUE,
    type_id INTEGER NOT NULL
);

CREATE TABLE Ingredient (
    id     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name  TEXT UNIQUE
);

CREATE TABLE Connection (
    recipe_id INTEGER NOT NULL,
    ingr_id INTEGER NOT NULL,
    PRIMARY KEY (recipe_id,ingr_id)
)

''')
