from bs4 import BeautifulSoup
import requests
import spacy
import pprint
import re


class RecipeFetcher:
    def scrape_recipe(self, recipe_url):
        results = {}
        page_html = requests.get(recipe_url)
        page_graph = BeautifulSoup(page_html.content, features="lxml")
        results['ingredients'] = [ingredient.text for ingredient in
                                  page_graph.find_all('span', {'itemprop': 'recipeIngredient'})]
        results['directions'] = [direction.text.strip() for direction in
                                 page_graph.find_all('span', {'class': 'recipe-directions__list--item'})
                                 if direction.text.strip()]
        return results

    def transform_quantity(self, q):
        if q == 'to taste' or q == 'as needed':
            return q
        split = q.split()
        total = 0
        for ea in split:
            if '/' in ea:
                num, denom = ea.split('/')
                total += int(num) / int(denom)
            else:
                total += float(ea)
        return total

    def scrape_ingredient(self, ingredient):
        nlp = spacy.load('en')
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
        return ' '.join(name), self.transform_quantity(quantity), measurement, ' '.join(descriptor), ' '.join(prep)

    def scrape_ingredients(self, ingredients):
        d = {}
        for ea in ingredients:
            name, quant, measure, descrip, prep = rf.scrape_ingredient(ea)
            d[name] = {'Quantity': quant, 'Measurement': measure, 'Descriptor': descrip, 'Preparation': prep}
        return d


pp = pprint.PrettyPrinter(indent=4)
rf = RecipeFetcher()
recipe = 'https://www.allrecipes.com/recipe/273326/parmesan-crusted-shrimp-scampi-with-pasta/?internalSource=previously%20viewed&referringContentType=Homepage&clickId=cardslot%202'
recipe = 'https://www.allrecipes.com/recipe/7721/katrinas-banana-cake/?internalSource=rotd&referringId=15827&referringContentType=Recipe%20Hub'
recipe = 'https://www.allrecipes.com/recipe/235432/creamy-herbed-pork-chops/'
recipe = 'https://www.allrecipes.com/recipe/218091/classic-and-simple-meat-lasagna/'
ingredients = {}
scraped = rf.scrape_recipe(recipe)
pp.pprint(rf.scrape_ingredients(scraped['ingredients']))
'''
for item in scraped:
    print('\n', item)
    for subitem in scraped[item]:
        print(subitem)
'''
