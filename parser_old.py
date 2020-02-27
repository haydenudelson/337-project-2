from bs4 import BeautifulSoup
import requests
import spacy
import pprint
import re
from unicodedata import numeric


# mostly from https://en.wikipedia.org/wiki/Cookware_and_bakeware
cookware = ['oven', 'stove', 'stovetop', 'convection oven',
            'braising pan', 'braiser', 'roaster', 'rondeau pan', 'cassarole pot', 'dilipot', 'frypan', 'skillet',
            'omelette pan', 'grill pan', 'waffle maker', 'saucepot', 'cake tin', 'cake pan', 'muffin tin',
            'swiss roll tin', 'pie pan',
            'comal', 'cookie sheet', 'double boiler', 'doufeu', 'dutch oven', 'food processor', 'griddle', 'karahi',
            'kazan', 'kettle', 'pan', 'baking pan', 'chip pan', 'crepe pan', 'frying pan', 'roasting pan',
            'saucepan', 'sauté pan', 'sheet pan', 'splayed sauté pan', 'springform pan', 'tube pan',
            'angel food cake pan', 'bundt cake pan', 'kugelhopf pan', 'pot', 'beanpot', 'cooking pot', 'stockpot',
            'wonder pot', 'pressure cooker', 'ramekin', 'roasting rack', 'saucier', 'soufflé dish', 'tajine', 'wok']

# from https://en.wikipedia.org/wiki/List_of_food_preparation_utensils
utensils = ['apple corer', 'apple cutter', 'baster', 'beanpot', 'biscuit press', 'blow torch', 'boil over preventer',
            'bottle opener', 'bowl', 'bread knife', 'browning tray', 'butter curler', 'cake and pie server',
            'cheese cutter', 'cheese knife', 'cheese slicer', 'cheesecloth', 'chef\'s knife', 'cherry pitter',
            'chinois', 'clay pot', 'cleaver', 'colander', 'cookie cutter', 'corkscrew', 'crab cracker', 'cutting board',
            'dough scraper', 'edible tableware', 'egg piercer', 'egg poacher', 'egg separator', 'egg slicer',
            'egg timer', 'fat separator', 'fillet knife', 'fish scaler', 'fish slice', 'flour sifter', 'food mill',
            'funnel', 'garlic press', 'grapefruit knife', 'grater', 'gravy strainer', 'herb chopper', 'honey dipper',
            'ladle', 'lame', 'lemon reamer', 'lemon squeezer', 'lobster pick', 'mandoline', 'mated colander pot',
            'measuring cup', 'measuring spoon', 'meat grinder', 'meat tenderiser', 'meat thermometer', 'melon baller',
            'mezzaluna', 'microplane', 'milk frother', 'mortar and pestle', 'nutcracker', 'nutmeg grater', 'oven glove',
            'pastry bag', 'pastry blender', 'pastry brush', 'pastry wheel', 'peel', 'peeler', 'pepper mill', 'pie bird',
            'pizza cutter', 'potato masher', 'potato ricer', 'pot-holder', 'poultry shears', 'roller docker',
            'rolling pin', 'salt shaker', 'scales', 'scissors', 'scoop', 'sieve', 'slotted spoon', 'spatula', 'spider',
            'sugar thermometer', 'tamis', 'tin opener', 'tomato knife', 'tongs', 'trussing needle', 'twine', 'whisk',
            'wooden spoon', 'zester']

tools = cookware + utensils


class RecipeFetcher:
    def scrape_recipe(self, recipe_url):
        results = {}
        page_html = requests.get(recipe_url)
        page_graph = BeautifulSoup(page_html.content, features="lxml")
        results['ingredients'] = [ingredient.text for ingredient in
                                  page_graph.find_all('span', {'itemprop': 'recipeIngredient'}) or
                                  page_graph.find_all('span', {'class': 'ingredients-item-name'})]
        results['directions'] = [direction.text.strip() for direction in
                                 page_graph.find_all('li', {'class': 'step'})
                                 or page_graph.find_all('li', {'class': 'subcontainer instructions-section-item'})]
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
                try:
                    total += float(ea)
                except ValueError:
                    total += numeric(ea)
        return total

    def scrape_ingredient(self, ingredient):
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
        return ' '.join(name), self.transform_quantity(quantity), measurement, ' '.join(descriptor), ' '.join(prep)

    def scrape_ingredients(self, ingredients):
        d = {}
        for ea in ingredients:
            name, quant, measure, descrip, prep = rf.scrape_ingredient(ea)
            d[name] = {'Quantity': quant, 'Measurement': measure, 'Descriptor': descrip, 'Preparation': prep}
        return d

    def scrape_tools(self, directions):
        nlp = spacy.load('en_core_web_sm')
        found_tools = []
        for direction in directions:
            # print(direction)
            tokenized = re.findall(r"\w+", direction)
            for tool in tools:
                tool_tokenized = re.findall(r"\w+", tool)
                if tool in direction and tool not in found_tools:
                    i = tokenized.index(tool_tokenized[0])
                    prev = tokenized[i-1]
                    doc = nlp('My ' + prev + ' ' + tool)
                    # print(doc)
                    tag = doc[1].pos_

                    'Add on any adjectives before the tool'
                    while tag == 'ADJ' and i > 0:
                        tool = prev + ' ' + tool
                        i -= 1
                        prev = tokenized[i - 1]
                        doc = nlp('My ' + prev + ' ' + tool)
                        tag = doc[1].pos_
                    found_tools.append(tool)

        # remove less specific tools (if there is both "pan" and "baking pan", remove "pan")
        for tool1 in found_tools:
            for tool2 in found_tools:
                if tool1 != tool2 and tool1 in tool2:
                    found_tools.remove(tool1)
        return found_tools


pp = pprint.PrettyPrinter(indent=4)
rf = RecipeFetcher()
recipe1 = 'https://www.allrecipes.com/recipe/273326/parmesan-crusted-shrimp-scampi-with-pasta/'
recipe2 = 'https://www.allrecipes.com/recipe/7721/katrinas-banana-cake/'
recipe3 = 'https://www.allrecipes.com/recipe/235432/creamy-herbed-pork-chops/'
recipe4 = 'https://www.allrecipes.com/recipe/218091/classic-and-simple-meat-lasagna/'
recipes = [recipe1, recipe2, recipe3, recipe4]
parsed = {}
for recipe in recipes:
    parsed[recipe] = {}
    scraped = rf.scrape_recipe(recipe)
    parsed[recipe]['ingredients'] = rf.scrape_ingredients(scraped['ingredients'])
    parsed[recipe]['tools'] = rf.scrape_tools(scraped['directions'])
    pp.pprint(parsed[recipe])
