import spacy
from unicodedata import numeric


def transform_quantity(q):
    if q == 'to taste' or q == 'as needed':
        return q
    split = q.split()
    total = 0
    for ea in split:
        if '/' in ea:
            num, denom = ea.split('/')
            total += int(num) / int(denom)
        else:
            try:
                total += float(ea)
            except ValueError:
                total += numeric(ea)
    return total


def scrape_ingredient(ingredient):
    nlp = spacy.load('en_core_web_sm')
    units = {'cup', 'teaspoon', 'tablespoon', 'pound', 'ounce', 'clove', 'jar', 'package', 'packet'}
    temp = set()
    for each in units:
        temp.add(each + 's')
    units |= temp
    list_of_ingr = ingredient.split()
    q, i = [], 0
    while list_of_ingr[i].replace('/', '').isnumeric():
        q.append(list_of_ingr[i])
        i += 1
    quantity = ' '.join(q) if q else 'as needed' if 'as needed' in q else 'to taste'
    m = []
    while list_of_ingr[i].strip('(),').replace('/', '').isnumeric() or list_of_ingr[i].strip('()') in units:
        m.append(list_of_ingr[i].strip('(),'))
        i += 1
    measurement = ' '.join(m)
    descriptor, prep, name = [x for x in list_of_ingr if '-' in x], [], []
    name_stopwords = {'shortening', 'baking', 'evaporated', 'condensed', 'garlic', 'onion'}
    descrip_stopwords = {'wheat'}
    ingr = ' '.join([x for x in list_of_ingr if '-' not in x][i:]).replace('to taste', '').replace('as needed', '')
    doc = nlp('I ate ' + ingr)
    for i in range(2, len(doc)):
        tag = doc[i].pos_
        word = str(doc[i])
        if word not in descrip_stopwords and (tag == 'NOUN' or tag == 'PROPN' or word in name_stopwords):
            name.append(word)
        elif tag == 'VERB':
            pre = ''
            if i > 0 and doc[i-1].pos_ == 'ADV':
                pre = str(doc[i-1]) + ' '
            prep.append(pre + word)
        elif tag == 'DET' or tag == 'ADJ' or word in descrip_stopwords:
            descriptor.append(word)
    if not name:
        if prep:
            name = prep
            prep = []
        elif descriptor:
            name = descriptor
            descriptor = []
        else:
            name = list_of_ingr[i:]
    return ' '.join(name), transform_quantity(quantity), measurement, ' '.join(descriptor), ' '.join(prep)


def scrape_ingredients(ingredients):
    d = {}
    for ea in ingredients:
        name, quant, measure, descrip, prep = scrape_ingredient(ea)
        d[name] = {'Quantity': quant, 'Measurement': measure, 'Descriptor': descrip, 'Preparation': prep}
    return d
