import pprint
from recipe_fetcher import RecipeFetcher
import ingredient_parser as ingred_parse
import tool_parser as tool_parse

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
    parsed[recipe]['ingredients'] = ingred_parse.scrape_ingredients(scraped['ingredients'])
    parsed[recipe]['tools'] = tool_parse.scrape_tools(scraped['directions'])
    pp.pprint(parsed[recipe])
