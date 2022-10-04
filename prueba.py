
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
        


def pizza_list(path):
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

for row in pizza_list('ingredients.txt'):
    print(create_pizza(row).name)
    print(create_pizza(row).ingredient_list)