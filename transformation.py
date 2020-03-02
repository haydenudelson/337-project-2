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
    "egg": "oat flour",
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
    "meatball": "beggie meatball",
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
    "egg":"egg white",
    "pasta":"multigrain pasta",
    "spaghetti":"multigrain spaghetti",
    "cheese":"low-fat cheese",
    "sour cream":"fat-free yogurt",
    "cream":"skim milk",
    "flour":"whole wheat flour",
    "all-purpose flour":"whole wheat flour",
    "couscous":"quinoa",
    "bread crumbs":"ground flaxseeds",
    "tortilla":"lettuce leaves",
    "oatmeal":"quinoa",
    "crouton":"almond",
    "chocolate chip":"cacao nib",
    "white wine":"red wine",
    "milk":"almond milk",
    "butter":"olive oil",
    "vegetable oil":"olive oil",
    "canola oil":"olive oil"
}

class Transformer:
    def to_vegetarian(self, recipe):
        # look at list of ingredients for meats
        # find corresponding step and replace meat ingredient with appropriate substitute

        print(recipe["steps"])

        ingredients = recipe["ingredients"].keys()
        for i in ingredients:
            if i in to_vegetarian:
                for s in recipe["steps"]:
                    if i in s:
                        s.replace(i, to_vegetarian[i])

        print(recipe["steps"])

        return None
    def from_vegetarian(self, recipe):
        ingredients = recipe["ingredients"].keys()

        for i in ingredients:
            if i in from_vegetarian:
                for s in recipe["steps"]:
                    if i in s:
                        s.replace(i, from_vegetarian[i])

        print(recipe["steps"])
    def to_healthy(self, recipe):
        return None
    def from_healthy(self, recipe):
        return None
    def to_chinese(self, recipe):
        return None