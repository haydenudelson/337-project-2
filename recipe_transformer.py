from transformation import *

def transform_recipe(recipe, option):
    if(option == 'To vegetarian'):
        to_vegetarian(recipe)
    elif(option == 'From vegetarian to non-vegetarian'):
        from_vegetarian(recipe)
    elif(option == 'To healthy'):
        to_healthy(recipe)
    elif(option == 'From healthy to un-healthy'):
        from_healthy(recipe)
    elif(option == 'To Chinese'):
        to_chinese(recipe)
    else:
        print("Not a valid transformation")

    return recipe
