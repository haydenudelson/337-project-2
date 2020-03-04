from transformation import Transformer


def transform_recipe(recipe, transformation):
    rt = Transformer()
    if transformation == 'To vegetarian':
        new_recipe = rt.to_vegetarian(recipe)
        return new_recipe
    elif transformation == 'From vegetarian to non-vegetarian':
        new_recipe = rt.from_vegetarian(recipe)
        return new_recipe
    elif transformation == 'To vegan':
        new_recipe = rt.to_vegan(recipe)
        return new_recipe
    elif transformation == 'To healthy':
        new_recipe = rt.to_healthy(recipe)
        return new_recipe
    elif transformation == 'From healthy to un-healthy':
        print(transformation + ' not implemented yet')
        return recipe
        # new_recipe = rt.from_healthy(recipe)
        # return new_recipe
    elif transformation == 'Double the recipe':
        new_recipe = rt.double(recipe)
        return new_recipe
    elif transformation == 'Halve the recipe':
        new_recipe = rt.halve(recipe)
        return new_recipe
    elif transformation == 'To chinese':
        new_recipe = rt.to_chinese(recipe)
        return new_recipe
    else:
        print(transformation + ' not implemented yet.')
        return recipe
