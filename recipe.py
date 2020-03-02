from pprint import PrettyPrinter
from recipe_parser import parsed_recipe
from recipe_transformer import transform_recipe


def print_recipe(input_recipe):
    pp = PrettyPrinter(indent=4)
    ingredients = input_recipe['ingredients']
    tools = input_recipe['tools']
    methods = input_recipe['methods']
    steps = input_recipe['steps']

    print('Ingredients: ')
    pp.pprint(ingredients)

    print('Tools: ')
    pp.pprint(tools)

    print('Methods: ')
    pp.pprint(methods)

    print('Steps: ')
    pp.pprint(steps)


options_list = ['To vegetarian',
                'From vegetarian to non-vegetarian',
                'To healthy',
                'From healthy to un-healthy',
                'To chinese',
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

    recipe = transform_recipe(recipe, choice)
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
