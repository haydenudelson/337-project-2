import re

cooking_techniques = ['dry roast', 'hot salt fry', 'sear', 'bake', 'roast', 'smoke', 'grill', 'rotisserie', 'toast',
                      'blanch', 'boil', 'decoct', 'parboil', 'shock', 'coddle', 'cream', 'infuse', 'poach', 'simmer',
                      'slow cook', 'smother', 'steep', 'stew', 'bain-marie', 'bain marie', 'double boil', 'sous-vide',
                      'sous vide', 'double steam', 'steam', 'blacken', 'brown', 'deep fry', 'pan fry', 'reduce',
                      'shallow fry', 'stir fry', 'sauté', 'gentle fry', 'sweat', 'barbecue', 'braise', 'flambé',
                      'fricassee', 'plank cook', 'air fry', 'microwave', 'pressure cook', 'pressure fry',
                      'thermal cook', 'cure', 'ferment', 'pickle', 'sour']


def scrape_methods(directions):
    methods = []
    for direction in directions:
        tokenized = re.findall(r"\w+", direction.lower())
        for word in tokenized:
            if word in cooking_techniques and word not in methods:
                methods.append(word)
    return methods
