from transformation import Transformer


def transform_recipe(recipe, transformation):
    rt = Transformer()
    if transformation == 'To vegetarian':
        new_recipe, changes = rt.to_vegetarian(recipe)
        return new_recipe, changes
    elif transformation == 'From vegetarian to non-vegetarian':
        new_recipe, changes = rt.from_vegetarian(recipe)
        return new_recipe, changes
    elif transformation == 'To vegan':
        new_recipe, changes = rt.to_vegan(recipe)
        return new_recipe, changes
    elif transformation == 'To healthy':
        new_recipe, changes = rt.to_healthy(recipe)
        return new_recipe, changes
    elif transformation == 'From healthy to un-healthy':
        new_recipe, changes = rt.from_healthy(recipe)
        return new_recipe, changes
    elif transformation == 'Double the recipe':
        new_recipe, changes = rt.double(recipe)
        return new_recipe, changes
    elif transformation == 'Halve the recipe':
        new_recipe, changes = rt.halve(recipe)
        return new_recipe, changes
    elif transformation == 'To chinese':
        new_recipe, changes = rt.to_chinese(recipe)
        return new_recipe, changes
    else:
        print(transformation + ' not implemented yet.')
        return recipe, 'None'
