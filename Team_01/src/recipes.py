import pandas as pd
from joblib import load

class Nutritionist:
    def __init__(self):
        self.model = load("data/VotingClassifier_0.79932.sav")
        self.similar_recipes = pd.read_csv("data/similar_recipes.csv")

    
    def get_ingredient_vector(self, available_ingredients, all_ingredients):
        return [1.0 if ingredient in available_ingredients else 0.0 for ingredient in all_ingredients]

    def prediction(self, list_print):
        LIST_NICE_COLUMS = list((pd.read_csv("data/ingredients.csv")).columns)
        list_print = list(str(x).strip().lower() for x in list_print)
        list_print= list(set(list_print) & set(LIST_NICE_COLUMS))

        ingredient_vector = self.get_ingredient_vector(list_print, LIST_NICE_COLUMS)
        X_new = pd.DataFrame([ingredient_vector], columns=LIST_NICE_COLUMS)

        if (self.model.predict(X_new) == 'bad'):
            print ('You might find it tasty, but in our opinion, it is a bad idea to have a dish with that list of ingredients.')
        elif (self.model.predict(X_new) == 'great'):
            print ('Excellent choice! This combination of ingredients has great potential.')
        else:
            print ('This is a borderline combination - it could go either way!')
        pass

    def print_nutrition(self, ingredient):
        nutrition_data = pd.read_csv("data/nutritions_facts.csv", index_col=0)
        ingredient = ingredient.strip().lower()
        nutrition_data.index = nutrition_data.index.astype(str).str.strip().str.lower()
        if ingredient in nutrition_data.index:
            return nutrition_data.loc[ingredient]
        return None
    
    def find_similar_recipes(self, recipe_vector, recipe_data, title_column):
        similarity = []
        for _, row in recipe_data.iterrows():
            similarity.append(self.count_matches(recipe_vector, row.values))
        df = recipe_data.copy()
        df["similarity"] = similarity

        top_recipes = df.sort_values(by='similarity', ascending=False).head(3)
        return self.similar_recipes[self.similar_recipes["title"].isin(title_column[top_recipes.index])]
        pass

    def count_matches(self, a, b):
        return sum(x == 1 and y == 1 for x, y in zip(a, b))

    def generate_daily_menu(self, num_samples=1000):
        LIST_NICE_COLUMS = ['title', 'rating', 'dinner', 'lunch', 'breakfast']
        titles = list((pd.read_csv("data/ingredients.csv")).columns) + LIST_NICE_COLUMS
        df = pd.read_csv('data/epi_r.csv')
        df = df[titles]
        
        nutr_facts = pd.read_csv("data/nutritions_facts.csv", index_col=0)
        nutr_facts.index = nutr_facts.index.astype(str).str.strip().str.lower()

        daily_df = pd.read_csv("data/daily.tsv", sep='\t')

        nutr_facts_cols = {c.strip().lower(): c for c in nutr_facts.columns}
        daily_norms = {}
        for _, row in daily_df.iterrows():
            norm_name = row['Nutrient'].strip().lower()
            try:
                value = float(str(row['Daily Value']).replace(',', '').strip())
            except Exception:
                continue
            if norm_name in nutr_facts_cols:
                daily_norms[nutr_facts_cols[norm_name]] = value
            else:
                for col in nutr_facts.columns:
                    if norm_name in col.strip().lower():
                        daily_norms[col] = value
                        break
        
        best_menus = []
        best_nutrition_score = float('-inf')
        best_menu = None
        
        for _ in range(num_samples):
            breakfast = df[df['breakfast'] == 1].sample(1).iloc[0]
            lunch = df[df['lunch'] == 1].sample(1).iloc[0]
            dinner = df[df['dinner'] == 1].sample(1).iloc[0]
            
            menu = [breakfast, lunch, dinner]
            
            total_nutrition = {nutrient: 0 for nutrient in daily_norms.keys()}
            
            for recipe in menu:
                recipe_ingredients = [col for col in df.columns if col not in LIST_NICE_COLUMS and recipe.get(col, 0) == 1]
                valid_ingredients = [ing for ing in recipe_ingredients if ing in nutr_facts.index]

                for nutrient in daily_norms.keys():
                    if nutrient in nutr_facts.columns:
                        total_nutrition[nutrient] += nutr_facts.loc[valid_ingredients, nutrient].fillna(0).sum()

            nutrition_score = 0
            for nutrient, value in total_nutrition.items():
                target = daily_norms[nutrient]
                if value < 0.8 * target:
                    nutrition_score -= (0.8 * target - value) / target
                elif value > 1.2 * target:
                    nutrition_score -= 2 * (value - 1.2 * target) / target
                else:
                    nutrition_score += 1
            
            if nutrition_score > best_nutrition_score:
                best_nutrition_score = nutrition_score
                best_menus = [(menu, sum(recipe['rating'] for recipe in menu))]
            elif nutrition_score == best_nutrition_score:
                best_menus.append((menu, sum(recipe['rating'] for recipe in menu)))

        if best_menus:
            best_menu, _ = max(best_menus, key=lambda x: x[1])
        else:
            best_menu = None

        meal_names = ['BREAKFAST', 'LUNCH', 'DINNER']
        result = []
        
        for i, recipe in enumerate(best_menu):
            title = recipe['title']
            rating = recipe['rating']

            url_row = self.similar_recipes[self.similar_recipes['title'].str.strip().str.lower() == str(title).strip().lower()]
            url = url_row['url'].values[0] if not url_row.empty else 'N/A'

            ingredients = [col for col in df.columns if col not in LIST_NICE_COLUMS and recipe.get(col, 0) == 1]
            valid_ingredients = [ing for ing in ingredients if ing in nutr_facts.index]

            nutr_info = {}
            nutr_pct = {}
            for nutrient in daily_norms.keys():
                if nutrient in nutr_facts.columns:
                    value = nutr_facts.loc[valid_ingredients, nutrient].fillna(0).sum()
                    nutr_info[nutrient] = value
                    nutr_pct[nutrient] = value / daily_norms[nutrient] * 100 if daily_norms[nutrient] else 0
  
            meal_str = f"{meal_names[i]}\n---------------------\n{title} (rating: {rating})\nIngredients:\n- {'\n- '.join(ingredients)}\nNutrients:" \
                + ''.join([f"\n- {n}: {nutr_pct[n]:.1f}%" for n in nutr_info.keys()]) \
                + f"\nURL: {url}"
            result.append(meal_str)
        
        print('DAILY MENU\n' + '\n\n'.join(result))
        return best_menu
