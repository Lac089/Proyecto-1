import sqlite3
import matplotlib.pyplot as plt

# Connect to Database pizza.sqlite
conn = sqlite3.connect('pizza.sqlite')
cur = conn.cursor()

# Functions

def time_histogram():
    #TODO 
    return 0

def recipe_histogram():
    #TODO 
    counts = dict()
    cur.execute('SELECT recipe_id FROM Pizza')
    recipe_list = cur.fetchall()
    for line in recipe_list:
        recipe_id = line[0]
        name =recipe_name(recipe_id)
        counts[name] = counts.get(name, 0) +1
    return counts

def avg_price():
    #TODO 
    return 0

def ingredients_histogram():
    #TODO 
    return 0

def size_histogram():
    #TODO 
    return 0

def recipe_name(recipe_id):
    cur.execute('SELECT name FROM Recipe WHERE id = ? ', (recipe_id,))
    recipe_id = cur.fetchone()[0]
    return recipe_id


# x axis values
x = []
# corresponding y axis values
y = []

for name,count in recipe_histogram().items():
    x = x + [name]
    y = y + [count]
# plotting the points 
plt.plot(x, y)
  
# naming the x axis
plt.xlabel('x - axis')
# naming the y axis
plt.ylabel('y - axis')
  
# giving a title to my graph
plt.title('My first graph!')
  
# function to show the plot
plt.show()
print(x)