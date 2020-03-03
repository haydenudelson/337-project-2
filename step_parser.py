def tag_things(direction, list_of_things):
    list_of_things = sorted(list_of_things, key=len, reverse=True)
    for i in range(len(list_of_things)):
        thing = list_of_things[i]
        if ' ' + thing + ' ' in direction:
            direction = direction.replace(thing, '\\*' + str(i) + '*\\')
    for i in range(len(list_of_things)):
        thing = list_of_things[i]
        direction = direction.replace('\\*' + str(i) + '*\\', '*' + thing + '*')
    return direction


def scrape_steps(directions, tools, ingredients, methods):
    steps = []
    for direction in directions:
        while '\n' in direction:
            direction = direction.replace('\n', ' ')
        while '  ' in direction:
            direction = direction.replace('  ', ' ')
        if direction in ['', ' ']:
            continue
        direction = tag_things(direction, tools)
        direction = tag_things(direction, ingredients)
        direction = tag_things(direction, methods)

        steps.append(direction)
    # print(steps)
    return steps
