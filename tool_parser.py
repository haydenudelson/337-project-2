import spacy
import re

# from https://en.wikipedia.org/wiki/Cookware_and_bakeware
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


def scrape_tools(directions):
    nlp = spacy.load('en_core_web_sm')
    found_tools = []
    for direction in directions:
        # print(direction)
        tokenized = re.findall(r"\w+", direction)
        for tool in tools:
            tool_tokenized = re.findall(r"\w+", tool)
            if tool in tokenized and tool not in found_tools:
                i = tokenized.index(tool_tokenized[0])
                prev = tokenized[i-1]
                doc = nlp('My ' + prev + ' ' + tool)
                # print(doc)
                tag = doc[1].pos_

                'Add on any adjectives before the tool'
                while tag == 'ADJ' and i > 0:
                    tool = prev + ' ' + tool
                    i -= 1
                    prev = tokenized[i-1]
                    doc = nlp('My ' + prev + ' ' + tool)
                    tag = doc[1].pos_
                found_tools.append(tool)

    # remove less specific tools (if there is both "pan" and "baking pan", remove "pan")
    for tool1 in found_tools:
        for tool2 in found_tools:
            if tool1 != tool2 and tool1 in tool2:
                found_tools.remove(tool1)
    return found_tools
