import pandas as pd
import numpy as np
import sys
from recipes import Nutritionist

def print_similar_recipes(list_print, processor, recipe_data, title_column):
    ingredient_columns = recipe_data.columns
    recipe_vector = np.zeros(len(ingredient_columns))

    for ingredient in list_print:
        if ingredient in recipe_data.columns:
            recipe_vector[recipe_data.columns.get_loc(ingredient)] = 1

    similar_recipes = processor.find_similar_recipes(recipe_vector, recipe_data, title_column)
    for _, row in similar_recipes.iterrows():
        print(f"- {row['title']}, rating: {row['rating']}, URL: {row['url']}")

def main():
    args = sys.argv[1:]
    input_string = ' '.join(sys.argv[1:])

    #Bonus
    if 'menu' in args:
        processor = Nutritionist()
        processor.generate_daily_menu(num_samples=1000)
        sys.exit(0)
    
    if not input_string.strip():
        print("No values provided. Exiting.")
        sys.exit(0)
    list_print = [item.strip() for item in input_string.split(',') if item.strip()]

    #I.
    print('I. OUR FORECAST')
    processor = Nutritionist()
    processor.prediction(list_print)
    
    #II.
    print('\nII. NUTRITION FACTS')
    for ingredient in list_print:
        nutrient = processor.print_nutrition(ingredient)
        if nutrient is not None:
            print(f"{ingredient.capitalize()}")
            for nutrient, value in nutrient.fillna(0).items():
                if value:
                    print(f"\t{nutrient} - {value}% of Daily Value")
        else:
            print(f"{ingredient.capitalize()} - No nutrition data available.")

    #III.
    print("III. TOP-3 SIMILAR RECIPES:")
    data = pd.read_csv("data/epi_r.csv")
    ingredient_columns = list(pd.read_csv("data/ingredients.csv").columns)
    ingredient_columns = [ingredient.strip() for ingredient in ingredient_columns]
    recipe_data = data[ingredient_columns]
    print_similar_recipes(list_print, processor, recipe_data, data["title"])

if __name__ == "__main__":
    main()
    
