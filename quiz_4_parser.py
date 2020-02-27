from bs4 import BeautifulSoup
import requests
import re


class RecipeFetcher:
    search_base_url = 'https://www.allrecipes.com/search/results/?wt=%s&sort=re'

    def search_recipes(self, keywords):
        search_url = self.search_base_url % (keywords.replace(' ', '+'))
        page_html = requests.get(search_url)
        page_graph = BeautifulSoup(page_html.content, features="lxml")
        return [recipe.a['href'] for recipe in page_graph.find_all('div', {'class': 'grid-card-image-container'})]

    def scrape_recipe(self, recipe_url):
        results = {}
        page_html = requests.get(recipe_url)
        page_graph = BeautifulSoup(page_html.content, features="lxml")
        results['ingredients'] = [ingredient.text for ingredient in
                                  page_graph.find_all('span', {'itemprop': 'recipeIngredient'})]
        results['directions'] = [direction.text.strip() for direction in
                                 page_graph.find_all('span', {'class': 'recipe-directions__list--item'})
                                 if direction.text.strip()]
        results['nutrition'] = self.scrape_nutrition_facts(recipe_url)
        return results

    def scrape_nutrition_facts(self, recipe_url):
        results = []
        nutrition_facts_url = '%s/fullrecipenutrition' % recipe_url
        page_html = requests.get(nutrition_facts_url)
        page_graph = BeautifulSoup(page_html.content, features="lxml")
        # r = re.compile("([0-9]*\.?[0-9]*)([a-zA-Z]+)")
        for nutrient_row in page_graph.find_all('div', {'class': 'nutrition-row'}):
            nutrient = {}
            stripped = nutrient_row.text.strip()

            nutrient_name, nutrient_value = stripped.split(': ')
            nutrient_unit = re.findall(r"[a-zA-Z]+", nutrient_value)[0]
            nutrient_value = re.findall(r"[0-9]*\.?[0-9]*", nutrient_value)[0]

            nutrient['name'] = nutrient_name
            nutrient['amount'] = nutrient_value
            nutrient['unit'] = nutrient_unit
            if '%' in stripped:
                nutrient['daily_value'] = re.findall(r"[0-9]*\.?[0-9]*\s%", stripped)[0]
            else:
                nutrient['daily_value'] = None

            results.append(nutrient)
        return results


rf = RecipeFetcher()
meat_lasagna = rf.search_recipes('meat lasagna')[0]
scraped = rf.scrape_recipe(meat_lasagna)
for item in scraped:
    print('\n', item)
    for subitem in scraped[item]:
        print(subitem)
