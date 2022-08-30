import sqlite3

conn = sqlite3.connect('pizza.sqlite')
cur = conn.cursor()

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