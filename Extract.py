import sqlite3
import csv
from unicodedata import name

# Classes


class Pizza:
    """A class used to represent each individual pizza

    Attributes
    ----------
    recipe_id : str
        a unique number that identifies the recipe of the pizza
    size : str
        the size of the pizza which can be S, M or L
    price : str
        the price of the pizza
    """


def __init__(self, recipe_id, size, price):
    """
    Parameters
    ----------
    recipe_id : str
        a unique number that identifies the recipe of the pizza
    size : str
        the size of the pizza which can be S, M or L
    price : str
        the price of the pizza
    """
    self.recipe_id = recipe_id
    self.size = size
    self.price = price


class Order:
    """A class used to represent each individual order

    Attributes
    ----------
    id : int
        a unique number that identifies the order
    date : str
        the date and time in yyy-mm-dd hh:mm:ss format
    """

    def __init__(self, id, date):
        """
        Parameters
        ----------
        id : int
        a unique number that identifies the order
        date : str
        the date and time in yyy-mm-dd hh:mm:ss format
        """
        self.id = id
        self.date = date

# Functions


def list_rows(path):
    """return a file as a list of rows

    Parameters
    ----------
    path : str
        the ath to the file to be opened
    Returns
    -------
    rows : list
        a list of the rows of the file
    """
    with open(path) as file:
        reader = csv.reader(file)
        rows = []
        for row in reader:
            rows.append(row)
        del rows[0]
        return rows


def real_date(date, time):
    """Receive a date in format 'mm/dd/yyyy' and a time and return a TIMESTAMP in format 'yyy-mm-dd hh:mm:ss'

    Parameters
    ----------
    date: ste
        String date in mm/dd/yyyy format
    time: str
        String time in hh:mm:ss

    Returns
    -------
    real : str
        the date and time in yyy-mm-dd hh:mm:ss format
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
    """Insert each unique type in the Type Table

    Parameters
    ----------
    date: str
        String date in mm/dd/yyyy format
    time: str
        String time in hh:mm:ss

    Returns
    -------
    type_id : str
        unique id of the type
    """
    cur.execute('''INSERT OR IGNORE INTO Type (name) VALUES ( ? )''', (type,))
    cur.execute('SELECT id FROM Type WHERE name = ? ', (type,))
    type_id = cur.fetchone()[0]
    return type_id


def ins_recipe(recipe, type_id):
    """Insert each unique recipe in the Recipe Table

    Parameters
    ----------
    recipe: str
        name of the recipe
    type_id: str
        unique id of the type

    Returns
    -------
    recipe_id : str
        unique id of the recipe
    """
    cur.execute(
        '''INSERT OR IGNORE INTO Recipe (name, type_id) VALUES ( ? , ? )''', (recipe, type_id))
    cur.execute('SELECT id FROM Recipe WHERE name = ? ', (recipe,))
    recipe_id = cur.fetchone()[0]
    return recipe_id


def ins_orders(order: Order):
    """Insert each unique order in the Order Table

    Parameters
    ----------
    order: Order
        object order to insert in the database
    """
    cur.execute(
        '''INSERT OR IGNORE INTO Orders (id, date) VALUES ( ? , ? )''', (order.id, order.date))


def ins_pizza(order: Order, pizza: Pizza):
    """Insert each unique pizza in the Pizza Table

    Parameters
    ----------
    order: Order
        order of the pizza
    pizza: Pizza
        object pizza to insert in the table
    """
    cur.execute('''INSERT OR IGNORE INTO Pizza (order_id, size, recipe_id, price ) VALUES ( ? , ?, ?, ?)''',
                (order.id, pizza.size, pizza.recipe_id, pizza.price))


def insert_ingredient(ingredient, recipe_id):
    """Insert each unique ingredient in the ingredient Table

    Parameters
    ----------
    ingredient: str
        name of the ingredient
    recipe_id: str
        unique id of the recipe
    """
    cur.execute(
        '''INSERT OR IGNORE INTO Ingredient (name) VALUES ( ? )''', (ingredient,))
    cur.execute('SELECT id FROM Ingredient WHERE name = ? ', (ingredient,))
    ing_id = int(cur.fetchone()[0])
    cur.execute(
        '''INSERT OR IGNORE INTO recipe_ingregients (recipe_id, ingr_id) VALUES ( ?,? )''', (ing_id, recipe_id))


def create_table_orders():
    """Create table orders"""
    cur.executescript('''
    CREATE TABLE IF NOT EXISTS Orders (
    id     INTEGER NOT NULL PRIMARY KEY UNIQUE,
    date     TIMESTAMP NOT NULL 
    )''')


def create_table_pizza():
    """Create table pizza"""
    cur.executescript('''CREATE TABLE IF NOT EXISTS Pizza (
    id     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    order_id INTEGER NOT NULL,
    size TEXT(1) NOT NULL,
    recipe_id INTEGER NOT NULL,
    price INTEGER NOT NULL)''')


def create_table_type():
    """Create table type"""
    cur.executescript('''
    CREATE TABLE IF NOT EXISTS Type (
    id     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name  TEXT UNIQUE)''')


def create_table_recipe():
    """Create table orders"""
    cur.executescript('''CREATE TABLE IF NOT EXISTS Recipe (
    id     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name  TEXT UNIQUE,
    type_id INTEGER NOT NULL)''')


def create_table_ingredient():
    """Create table ingredients"""
    cur.executescript('''CREATE TABLE IF NOT EXISTS Ingredient (
    id     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name  TEXT UNIQUE)''')


def create_table_recipe_ingregients():
    """Create table recipe_ingregients"""
    cur.executescript('''CREATE TABLE IF NOT EXISTS recipe_ingregients (
    recipe_id INTEGER NOT NULL,
    ingr_id INTEGER NOT NULL,
    PRIMARY KEY (recipe_id,ingr_id))''')


# Create Database pizza.sqlite
conn = sqlite3.connect('pizza.sqlite')
cur = conn.cursor()


# Create tables for orders, individual pizzas, recipes, types and a recipe_ingregients table  for ingredients
create_table_pizza()
create_table_orders()
create_table_type()
create_table_recipe()
create_table_ingredient()
create_table_recipe_ingregients()

# Open file Orders.csv and create the list of rows
rows = list_rows('Orders.csv')

# extract the orderid, date, size, recipe, price, and type of the pizza
# create the objects order and pizza and insert them in the database
for row in rows:
    pos = row[1].find('-')
    type_id = ins_type(row[6])
    recipe_id = ins_recipe(row[4], type_id)
    order = Order(int(row[1][pos+1:]), real_date(row[1], row[2]))
    pizza = Pizza(recipe_id, row[5], row[7])
    ins_orders(order)
    ins_pizza(order, pizza)
conn.commit()

with open('ingredients.txt') as filehandle:
    # read the file ingredients.txt and insert each ingredient in the database
    for line in filehandle:
        if len(line) == 1:
            continue
        pos = line.find(':')
        recipe = line[:pos]
        cur.execute('SELECT id FROM Recipe WHERE name = ? ', (recipe, ))
        recipe_id = int(cur.fetchone()[0])
        ingredients = line[pos+2:].split(", ")
        for ing in ingredients:
            insert_ingredient(ing, recipe_id)
    conn.commit()
