import copy

sample_recipe = {
    'ingredients': {
        'name': {
            'quantity': '',
            'measurement': ''
        }
    },
    'tools': ["knife", "pan"],
    'methods': ['boil'],
    'steps': ['']
}

# From, in part, Wikipedia's List of Meat Substitutes
to_vegan_list = {
    "milk": "oat milk",
    "cottage cheese": "crumbled tofu",
    "ricotta cheese": "crumbled tofu",
    "mozzarella cheese": "daiya mozzarella",
    "scrambled egg": "tofu scramble",
    "egg": "oat flour", "eggs": "oat flour",
    "butter": "olive oil",
    "cheese": "tofu (crumbled)"
}

to_vegetarian_list = {
    "beef stock": "vegetable broth",
    "chicken stock": "vegetable broth",
    "pork stock": "vegetable broth",
    "chicken broth": "vegetable broth",
    "beef broth": "vegetable broth",
    "pork broth": "vegetable broth",
    "chicken bouillon": "vegetable bouillon",
    "beef bouillon": "vegetable bouillon",
    "pork bouillon": "vegetable bouillon",
    "meatball": "veggie meatball",
    "sausage link": "veggie sausage link",
    "bacon":"veggie bacon",
    "burger":"veggie burger",
    "hamburger":"veggie burger",
    "sausage":"glamorgan sausage",
    "pork":"jackfruit",
    "pork tenderloin": "jackfruit",
    "pepperoni":"vegetable deli slice",
    "pastrami":"vegetable deli slice",
    "chicken breast":"tofu",
    "chicken thigh":"tofu",
    "chicken nuggets":"soy nuggets",
    "chicken":"tempeh",
    "beef":"tofurkey",
    "ground beef":"soy protein",
    "steak":"portebllo mushrooms",
    "ribs":"portebello mushrooms",
    "veal":"tofurkey",
    "lamb":"tofurkey",
    "turkey":"tofurkey",
    "tuna":"tempeh",
    "salmon":"tempeh",
    "scallop": "king oyster mushroom",
    "spam": "soy protein",
    "crab": "tofu",
    "haddock": "tempeh",
    "cod": "tempeh",
    "mackerel": "tempeh"
}

from_vegetarian_list ={
    "vegetable broth":"chicken broth",
    "vegetable bouillon":"chicken bouillon",
    "tempeh": "chicken",
    "jackfruit": "pork",
    "tofurkey":"turkey",
    "soy protein":"ground beef",
    "king oyster mushroom":"scallop",
    "vegetable deli slice":"pepperoni",
    "veggie meatball":"meatball",
    "veggie bacon":"bacon",
    "veggie burger":"burger"
}

# based in part on https://www.thespruceeats.com/chinese-cooking-ingredient-substitutions-4057957
to_chinese_list = {
    "olive oil": "peanut oil",
    "vegetable oil": "peanut oil",
    "canola oil": "peanut oil",
    "coconut oil": "peanut oil",
    "pasta": "lo mein",
    "spaghetti": "lo mein",
    "fettucini": "lo mein",
    "penne": "lo mein",
    "chives": "green onion",
    "parsley": "green onion",
    "basil": "green onion",
    "worcestershire sauce": "soy sauce",
    "hot sauce": "chili sauce",
    "red pepper": "chili paste",
    "vinegar": "chinkiang vinegar",
    "broccoli": "bok choy",
    "cabbage": "bok choy",
    "gelatin": "agar-agar",
    "carrot": "bamboo shoot",
    "asparagus": "bamboo shoot",
    "whole milk": "coconut milk",
    "milk": "coconut milk",
    "half-and-half": "coconut cream",
    "whipping cream": "coconut cream",
    "cornstarch": "lotus root flour",
    "oyster sauce": "soy sauce",
    "sherry vinegar": "rice vinegar"
}

# https://brighamhealthhub.org/healthy-living/ten-simple-substitutes-for-healthy-eating
# https://greatist.com/health/83-healthy-recipe-substitutions#Gluten-Free-Swaps
to_healthy_list = {
    "white rice": "brown rice",
    "egg": "egg white", "eggs": "egg whites",
    "pasta": "multigrain pasta",
    "spaghetti": "multigrain spaghetti",
    "cheese": "low-fat cheese",
    "sour cream": "fat-free yogurt",
    "cream": "skim milk",
    "flour": "whole wheat flour",
    "all-purpose flour": "whole wheat flour",
    "couscous": "quinoa",
    "bread crumbs": "ground flaxseeds",
    "tortilla": "lettuce leaves", "tortillas": "lettuce leaves",
    "oatmeal": "quinoa",
    "crouton": "almond", "croutons": "almonds",
    "chocolate chip": "cacao nib",
    "white wine": "red wine",
    "milk": "almond milk",
    "butter": "olive oil",
    "vegetable oil": "olive oil",
    "canola oil": "olive oil"
}

from_healthy_list: {
    "brown rice":"white rice",
    "egg white":"egg",
    "egg whites":"eggs",
    "olive oil":"butter"
}



class Transformer:
    def replace_ingredient(self, recipe, old_ing, new_ing):
        recipe["ingredients"][new_ing] = recipe["ingredients"][old_ing]
        del recipe["ingredients"][old_ing]
        for i in range(len(recipe["steps"])):
            step = recipe["steps"][i]
            recipe["steps"][i] = step.replace(old_ing, new_ing)
        return recipe

    def transform_on_list(self, recipe, list):
        ingredients = copy.deepcopy(recipe["ingredients"])

        changes = []

        for ing in recipe["ingredients"].keys():
            for item in list:
                if item in ing:
                    changes.append([ing, list[item]])
                    ingredients[list[item]] = ingredients.pop(ing)
                    for j in range(len(recipe["steps"])):
                        step = recipe["steps"][j]
                        recipe["steps"][j] = step.replace(item, list[item])
                    break

        recipe["ingredients"] = ingredients
        return recipe, changes


    def to_vegetarian(self, recipe):
        # look at list of ingredients for meats
        # find corresponding step and replace meat ingredient with appropriate substitute

        return self.transform_on_list(recipe, to_vegetarian_list)

    def from_vegetarian(self, recipe):
        return self.transform_on_list(recipe, from_vegetarian_list)

    def to_healthy(self, recipe):
        return self.transform_on_list(recipe, to_healthy_list)

    def from_healthy(self, recipe):
        return self.transform_on_list(recipe, from_healthy_list)

    def to_chinese(self, recipe):
        return self.transform_on_list(recipe, to_chinese_list)

    def double(self, recipe):
        for ingredient in recipe['ingredients']:
            quantity = recipe['ingredients'][ingredient]['Quantity']
            if isinstance(quantity, int) or isinstance(quantity, float):
                recipe['ingredients'][ingredient]['Quantity'] = quantity * 2
        return recipe, 'Doubled everything'

    def halve(self, recipe):
        for ingredient in recipe['ingredients']:
            quantity = recipe['ingredients'][ingredient]['Quantity']
            if isinstance(quantity, int) or isinstance(quantity, float):
                recipe['ingredients'][ingredient]['Quantity'] = quantity * 0.5
        return recipe, 'Halved everything'

    def to_vegan(self, recipe):
        temp_recipe, changes = self.transform_on_list(recipe, to_vegetarian_list)
        temp_recipe, changes2 = self.transform_on_list(temp_recipe, to_vegan_list)
        return temp_recipe, changes + changes2
