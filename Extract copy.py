import sqlite3
import csv
from typing import List
from unicodedata import name

# Classes


class Pizza:
    """A class used to represent each individual pizza

    Attributes
    ----------
    name : str
        a unique name that identifies the pizza recipe
    ingredient_list : list
        The list of the ingredients of the recipe
    """
    def __init__(self, name : str, ingredient_list : list):
        """
        Parameters
        ----------
        name : str
            a unique name that identifies the pizza recipe
        ingredient_list : list
            The list of the ingredients of the recipe
        """
        self.name = name
        self.ingredient_list = ingredient_list
        


class Order:
    """A class used to represent each individual order

    Attributes
    ----------
    id : int
        a unique number that identifies the order
    date : str
        the date and time in yyy-mm-dd hh:mm:ss format
    """

    def __init__(self, id : str, date : str, time : str, recipe : str, size : str, type : str, price : str):
        """
        Parameters
        ----------
        id : int
            a unique number that identifies the order
        date : str
            the date and time in yyy-mm-dd hh:mm:ss format
        time : str
            The time at which the order was places
        recipe : str
            The piza recipe of the order
        size : str
            The size of the order, it can be S, M, or L
        type : str
            The type of the pizza recipe
        price : str
            The price of the pizza on the order
        """
        self.id = id
        self.date = date
        self.time = time
        self.recipe = recipe
        self.size = size
        self.type = type
        self.price = price

# Functions


def list_rows(path):
    """return a csv file as a list of rows

    Parameters
    ----------
    path : str
        the path to the file to be opened
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



def pizza_list(path):
    """return a txt file as a list of rows

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
        lines = file.readlines()
        rows = []
        for row in lines:
            if len(row)>1:
                rows.append(row.strip('\n]'))
        return rows
            
def create_pizza(row : str):
    """return a Pizza class object representing the row of the file

    Parameters
    ----------
    row : str
        an string with the information of the pizza
    Returns
    -------
    pizza : Pizza
        Pizza class object representing the row of the file
    """
    line = row.split()
    name = line[0].strip(':')
    ingredient_list = []
    i = 0
    for ingredient in line:
        if i == 0:
            i = 1
            continue
        ingredient_list.append(ingredient.strip(','))
    pizza = Pizza(name, ingredient_list)
    return pizza

    
def ins_recipe(recipe):
    """Insert each unique recipe in the Recipe Table

    Parameters
    ----------
    recipe: str
        name of the recipe

    Returns
    -------
    recipe_id : str
        unique id of the recipe
    """
    cur.execute(
        '''INSERT OR IGNORE INTO Recipe (name) VALUES ( ? )''', (recipe, ))
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
        '''INSERT OR IGNORE INTO Orders (id, date, time) VALUES ( ? , ? , ?)''', (order.id, order.date, order.time))


def ins_pizza(order: Order):
    """Insert each unique pizza in the Pizza Table

    Parameters
    ----------
    order: Order
        order of the pizza
    """
    cur.execute('''INSERT OR IGNORE INTO Pizza (order_id, size, recipe_id, price ) VALUES ( ? , ?, ?, ?)''',
                (order.id, order.size, order.recipe, order.price))


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
        '''INSERT OR IGNORE INTO recipe_ingredients (recipe_id, ingr_id) VALUES ( ?,? )''', (ing_id, recipe_id))


def create_table_orders():
    """Create table orders"""
    cur.executescript('''
    CREATE TABLE IF NOT EXISTS Orders (
    id     TEXT NOT NULL PRIMARY KEY UNIQUE,
    date     TEXT NOT NULL,
    time    TEXT NOT NULL

    )''')


def create_table_pizza():
    """Create table pizza"""
    cur.executescript('''CREATE TABLE IF NOT EXISTS Pizza (
    id     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    order_id INTEGER NOT NULL,
    size TEXT(1) NOT NULL,
    recipe_id INTEGER NOT NULL,
    price INTEGER NOT NULL)''')



def create_table_recipe():
    """Create table orders"""
    cur.executescript('''CREATE TABLE IF NOT EXISTS Recipe (
    id     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name  TEXT UNIQUE
    )''')


def create_table_ingredient():
    """Create table ingredients"""
    cur.executescript('''CREATE TABLE IF NOT EXISTS Ingredient (
    id     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name  TEXT UNIQUE)''')


def create_table_recipe_ingredients():
    """Create table recipe_ingredients"""
    cur.executescript('''CREATE TABLE IF NOT EXISTS recipe_ingredients (
    recipe_id INTEGER NOT NULL,
    ingr_id INTEGER NOT NULL,
    PRIMARY KEY (recipe_id,ingr_id))''')


# Create Database pizza.sqlite
conn = sqlite3.connect('pizza.sqlite')
cur = conn.cursor()


# Create tables for orders, individual pizzas, recipes, types and a recipe_ingredients table  for ingredients
create_table_pizza()
create_table_orders()
create_table_recipe()
create_table_ingredient()
create_table_recipe_ingredients()

# Open files Orders.csv and ingredients.txt to extract the information in two lists
rows = list_rows('Orders.csv')
pizza_rows = pizza_list('ingredients.txt')

# extract the orderid, date, size, recipe, price, and type of the pizza
# create the objects order and pizza and insert them in the database
for row in rows:
    pos = row[1].find('-')
    recipe_id = ins_recipe(row[4])
    order = Order(row[1], row[2], row[3], row[4], row[5], row[6], row[7])
    ins_orders(order)
    ins_pizza(order)
conn.commit()

for row in pizza_rows:
    pizza = create_pizza(row)
    cur.execute('SELECT id FROM Recipe WHERE name = ? ', (pizza.name, ))
    recipe_id = int(cur.fetchone()[0])
    for ing in pizza.ingredient_list:
        insert_ingredient(ing, recipe_id)

    conn.commit()
