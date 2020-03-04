sample_recipe = {
    'ingredients':{
        'name':{
            'quantity':'',
            'measurement':''
        }
    },
    'tools': ["knife", "pan"],
    'methods':['boil'],
    'steps':['']
}

# From, in part, Wikipedia's List of Meat Substitutes
to_vegan = {
    "milk": "oat milk",
    "cottage cheese": "crumbled tofu",
    "ricotta cheese": "crumbled tofu",
    "mozzarella cheese": "daiya mozzarella",
    "scrambled egg": "tofu scramble",
    "egg": "oat flour", "eggs": "oat flour",
    "butter":"olive oil",
    "cheese":"tofu (crumbled)",

}

to_vegetarian = {
    "beef stock": "vegetable broth",
    "chicken stock": "vegetable broth",
    "pork stock": "vegetable broth",
    "chicken bouillon":"vegetable bouillon",
    "beef bouillon":"vegetable bouillon",
    "pork bouillon":"vegetable bouillon",
    "meatball": "veggie meatball",
    "sausage link": "veggie sausage link",
    "bacon":"veggie bacon",
    "burger":"veggie burger",
    "hamburger":"veggie burger",
    "sausage":"glamorgan sausage",
    "pork":"jackfruit",
    "pepperoni":"vegetable deli slice",
    "pastrami":"vegetable deli slice",
    "chicken":"tempeh",
    "chicken breast":"tofu",
    "chicken thigh":"tofu",
    "chicken nuggets":"soy nuggets",
    "beef":"tofurkey",
    "ground beef":"soy protein",
    "steak":"portebllo mushrooms",
    "ribs":"portebello mushrooms",
    "veal":"tofurkey",
    "lamb":"tofurkey",
    "turkey":"tofurkey",
    "tuna":"tempeh",
    "salmon":"tempeh",
    "spam":"soy protein",
    "crab":"tofu",
    "haddock":"tempeh",
    "cod":"tempeh",
    "mackerel":"tempeh"
}

from_vegetarian ={
    "vegetable broth":"chicken broth",
    "vegetable bouillon":"chicken bouillon"
}

#based in part on https://www.thespruceeats.com/chinese-cooking-ingredient-substitutions-4057957
to_chinese = {
    "olive oil":"peanut oil",
    "vegetable oil":"peanut oil",
    "canola oil":"peanut oil",
    "coconut oil":"peanut oil",
    "pasta":"lo mein",
    "spaghetti":"lo mein",
    "fettucini":"lo mein",
    "penne":"lo mein",
    "chives":"green onion",
    "parsley":"green onion",
    "basil":"green onion",
    "worcestershire sauce":"soy sauce",
    "hot sauce":"chili sauce",
    "red pepper":"chili paste",
    "vinegar":"chinkiang vinegar",
    "broccoli":"bok choy",
    "cabbage":"bok choy",
    "gelatin":"agar-agar",
    "carrot":"bamboo shoot",
    "asparagus":"bamboo shoot",
    "whole milk":"coconut milk",
    "milk":"coconut milk",
    "half-and-half":"coconut cream",
    "whipping cream":"coconut cream",
    "cornstarch":"lotus root flour",
    "oyster sauce":"soy sauce",
    "sherry vinegar":"rice vinegar"
}

#https://brighamhealthhub.org/healthy-living/ten-simple-substitutes-for-healthy-eating
#https://greatist.com/health/83-healthy-recipe-substitutions#Gluten-Free-Swaps
to_healthy = {
    "white rice":"brown rice",
    "egg":"egg white", "eggs":"egg whites",
    "pasta":"multigrain pasta",
    "spaghetti":"multigrain spaghetti",
    "cheese":"low-fat cheese",
    "sour cream":"fat-free yogurt",
    "cream":"skim milk",
    "flour":"whole wheat flour",
    "all-purpose flour":"whole wheat flour",
    "couscous":"quinoa",
    "bread crumbs":"ground flaxseeds",
    "tortilla":"lettuce leaves", "tortillas":"lettuce leaves",
    "oatmeal":"quinoa",
    "crouton":"almond", "croutons":"almonds",
    "chocolate chip":"cacao nib",
    "white wine":"red wine",
    "milk":"almond milk",
    "butter":"olive oil",
    "vegetable oil":"olive oil",
    "canola oil":"olive oil"
}

class Transformer:
    def replace_ingredient(self, recipe, old_ing, new_ing):
        recipe["ingredients"][new_ing] = recipe["ingredients"][old_ing]
        del recipe["ingredients"][old_ing]
        for i in range(len(recipe["steps"])):
            step = recipe["steps"][i]
            recipe["steps"][i] = step.replace(old_ing, new_ing)
        return recipe

    def to_vegetarian(self, recipe):
        # look at list of ingredients for meats
        # find corresponding step and replace meat ingredient with appropriate substitute

        # print(recipe["steps"])

        ingredients = recipe["ingredients"].keys()
        changed_ingredients = []
        for i in ingredients:
            if i in to_vegetarian:
                changed_ingredients.append([i, to_vegetarian[i]])
        for changed in changed_ingredients:
            old_i = changed[0]
            new_i = changed[1]
            recipe = self.replace_ingredient(recipe, old_i, new_i)

        # print(recipe["steps"])

        return recipe

    def from_vegetarian(self, recipe):
        ingredients = recipe["ingredients"].keys()

        changed_ingredients = []
        for i in ingredients:
            if i in from_vegetarian:
                changed_ingredients.append([i, from_vegetarian[i]])
        for changed in changed_ingredients:
            old_i = changed[0]
            new_i = changed[1]
            recipe = self.replace_ingredient(recipe, old_i, new_i)

        return recipe

    def to_healthy(self, recipe):
        ingredients = recipe["ingredients"].keys()

        changed_ingredients = []
        for i in ingredients:
            if i in to_healthy:
                changed_ingredients.append([i, to_healthy[i]])
        for changed in changed_ingredients:
            old_i = changed[0]
            new_i = changed[1]
            recipe = self.replace_ingredient(recipe, old_i, new_i)

        return recipe

    def from_healthy(self, recipe):
        return recipe

    def to_chinese(self, recipe):
        ingredients = recipe["ingredients"].keys()

        changed_ingredients = []
        for i in ingredients:
            if i in to_chinese:
                changed_ingredients.append([i, to_chinese[i]])
        for changed in changed_ingredients:
            old_i = changed[0]
            new_i = changed[1]
            recipe = self.replace_ingredient(recipe, old_i, new_i)

        return recipe

    def double(self, recipe):
        for ingredient in recipe['ingredients']:
            quantity = recipe['ingredients'][ingredient]['Quantity']
            if isinstance(quantity, int) or isinstance(quantity, float):
                recipe['ingredients'][ingredient]['Quantity'] = quantity * 2
        return recipe

    def halve(self, recipe):
        for ingredient in recipe['ingredients']:
            quantity = recipe['ingredients'][ingredient]['Quantity']
            if isinstance(quantity, int) or isinstance(quantity, float):
                recipe['ingredients'][ingredient]['Quantity'] = quantity * 0.5
        return recipe

    def to_vegan(self, recipe):
        recipe = self.to_vegetarian(recipe)
        ingredients = recipe["ingredients"].keys()

        changed_ingredients = []
        for i in ingredients:
            if i in to_vegan:
                changed_ingredients.append([i, to_vegan[i]])
        for changed in changed_ingredients:
            old_i = changed[0]
            new_i = changed[1]
            recipe = self.replace_ingredient(recipe, old_i, new_i)

        return recipe
