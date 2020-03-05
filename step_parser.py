import nltk

def tag_things(direction, list_of_things):
    list_of_things = sorted(list_of_things, key=len, reverse=True)
    for i in range(len(list_of_things)):
        thing = list_of_things[i]
        for character in [' ', '.', '.', ';']:
            string = ' ' + thing + character
            if string in direction:
                direction = direction.replace(string, ' \\*' + str(i) + '*\\' + character)
    for i in range(len(list_of_things)):
        thing = list_of_things[i]
        direction = direction.replace('\\*' + str(i) + '*\\', '*' + thing + '*')
    return direction


def scrape_steps(directions, tools, ingredients, methods):
    steps = []
    for big_direction in directions:
        for direction in nltk.sent_tokenize(big_direction):
            to_tag = tools + list(ingredients.keys()) + methods
            new_direction = tag_things(direction, to_tag)

            steps.append(new_direction)
    return steps
