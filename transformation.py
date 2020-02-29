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


to_vegetarian = {
    "milk": "oat milk",
    "cottage cheese": "crumbled tofu",
    "ricotta cheese": "crumbled tofu",
    "mozzarella cheese": "daiya mozzarella",
    "scrambled egg": "tofu scramble",
    "egg": "oat flour",
    "beef stock": "vegetable broth",
    "chicken stock": "vegetable broth",
    "butter":"olive oil",
    "meatball": "beggie meatball",
    "sausage link": "veggie sausage link",
    "bacon":"veggie bacon"
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
                        s.replace("i", to_vegetarian[i])

        print(recipe["steps"])

        return None
    def from_vegetarian(self, recipe):
        return None
    def to_healthy(self, recipe):
        return None
    def from_healthy(self, recipe):
        return None
    def to_chinese(self, recipe):
        return None