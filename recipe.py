from pprint import PrettyPrinter
from recipe_parser import parsed_recipe
from recipe_transformer import transform_recipe
from fractions import Fraction


def print_recipe(input_recipe):
    pp = PrettyPrinter(indent=4)
    ingredients = input_recipe['ingredients']
    tools = input_recipe['tools']
    methods = input_recipe['methods']
    steps = input_recipe['steps']
    
    print('\nIngredients')
    for ingredient in ingredients:
        desc = ingredients[ingredient]['Descriptor']
        meas = ingredients[ingredient]['Measurement']
        prep = ingredients[ingredient]['Preparation']
        quantity = ingredients[ingredient]['Quantity']
        to_print = ''
        if quantity != 'to taste':
            if quantity % 1 and quantity > 1:
                to_print += str(int(quantity - (quantity % 1))) + ' '
                to_print += str(Fraction(quantity % 1)) + ' '
            else:
                to_print += str(Fraction(quantity)) + ' '
        if meas:
            to_print += meas + ' '
        if prep:
            to_print += prep + ' '
        if desc:
            to_print += desc + ' '
        to_print += ingredient
        if quantity == 'to taste':
            to_print += ' (to taste)'
        print(to_print)

    print('\nTools')
    to_print = ''
    first_tool = True
    for tool in tools:
        if first_tool:
            to_print += tool
            first_tool = False
        else:
            to_print += ', ' + tool
    print(to_print)

    print('\nMethods')
    to_print = ''
    first_method = True
    for method in methods:
        if first_method:
            to_print += method
            first_method = False
        else:
            to_print += ', ' + method
    print(to_print)

    print('\nSteps')
    for step in range(len(steps)):
        print('Step ' + str(step + 1) + '. ' + steps[step])


def print_changes(changed):
    print('\nChanges During Transformation')
    if not changed:
        print('None')
        return
    if isinstance(changed, str):
        print(changed)
    else:
        for change in changed:
            print('Substituted ' + change[1] + ' for ' + change[0])


options_list = ['To vegetarian',
                'From vegetarian to non-vegetarian',
                'To healthy',
                'From healthy to un-healthy',
                'To chinese',
                'Double the recipe',
                'Halve the recipe',
                'To vegan']

options = ''
for i in range(len(options_list)):
    options += str(i+1) + '. ' + options_list[i] + '\n'

recipe = False
while True:
    if not recipe:
        url = input('Enter recipe URL: ')
        recipe = parsed_recipe(url)
        print_recipe(parsed_recipe(url))

    option = input('Choose a transformation:\n' + options)
    choice = 'Error, this should never be printed'
    try:
        i = int(option)
        choice = options_list[i-1]
    except:
        print('Well, I crashed. Make sure you choose a valid number next time.')
        break

    print('You chose: ' + choice)

    recipe, changes = transform_recipe(recipe, choice)
    print_changes(changes)
    print_recipe(recipe)

    choice = input('Would like to continue transforming the recipe or start from scratch with a new recipe?\n'
                   '1. Continue transforming\n'
                   '2. Start from scratch\n'
                   '3. Quit\n')
    if choice == '3':
        break
    elif choice == '2':
        recipe = False
    elif choice != '1':
        print('What was that? Did you say continue? Ok, then.')
