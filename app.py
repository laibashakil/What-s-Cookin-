import streamlit as st
import pandas as pd

# Load the cleaned dataset
df = pd.read_csv('cleaned_recipes.csv')

# Title of the app
st.title("What's Cookin'")

# Sidebar for filtering
st.sidebar.header('Filter Recipes')

# Multi-select for categories with placeholder
categories = st.sidebar.multiselect(
    'Select Category/Categories', 
    df['Category'].unique().tolist(), 
    help="Choose one or more categories to filter the recipes"
)

# Input for ingredients (optional)
ingredients_input = st.sidebar.text_input("Enter ingredients (comma-separated):", "")

# Inputs for other details
prep_time = st.sidebar.slider("Maximum Prep Time (minutes):", 0, 120, 60)
cook_time = st.sidebar.slider("Maximum Cook Time (minutes):", 0, 300, 60)
servings = st.sidebar.slider("Minimum Servings:", 1, 10, 2)

# Dietary preferences
st.sidebar.header('Dietary Preferences')
vegetarian = st.sidebar.checkbox("Vegetarian")
vegan = st.sidebar.checkbox("Vegan")
gluten_free = st.sidebar.checkbox("Gluten-free")

# Allergen filters (multi-select)
st.sidebar.header('Allergen Filters')
allergen_options = ['Peanuts', 'Shellfish', 'Dairy', 'Sugar', 'Eggs', 'Soy']
selected_allergens = st.sidebar.multiselect("Select allergens to exclude", allergen_options)

# Function to match ingredients and return matched ingredients
def match_ingredients(recipe_ingredients, user_ingredients):
    matched_ingredients = [ingredient for ingredient in user_ingredients if ingredient in recipe_ingredients.lower()]
    return matched_ingredients

# Function to filter recipes based on dietary preferences
def filter_dietary_preferences(ingredients, vegetarian, vegan, gluten_free):
    ingredients_lower = ingredients.lower()
    
    # Vegetarian filter: exclude meat and fish
    if vegetarian and any(item in ingredients_lower for item in ['chicken', 'beef', 'pork', 'fish', 'meat', 'shrimp']):
        return False
    # Vegan filter: exclude meat, fish, eggs, and dairy
    if vegan and any(item in ingredients_lower for item in ['chicken', 'beef', 'pork', 'fish', 'meat', 'shrimp', 'egg', 'milk', 'cheese', 'butter']):
        return False
    # Gluten-free filter: exclude ingredients with gluten (wheat, barley, rye)
    if gluten_free and any(item in ingredients_lower for item in ['wheat', 'barley', 'rye', 'malt', 'soy sauce']):
        return False
    return True

# Function to filter recipes based on selected allergens
def filter_allergens(ingredients, selected_allergens):
    ingredients_lower = ingredients.lower()
    
    # Check for each selected allergen
    if 'Peanuts' in selected_allergens and 'peanut' in ingredients_lower:
        return False
    if 'Shellfish' in selected_allergens and any(item in ingredients_lower for item in ['shrimp', 'prawn', 'lobster', 'crab']):
        return False
    if 'Dairy' in selected_allergens and any(item in ingredients_lower for item in ['milk', 'cheese', 'butter', 'yogurt', 'cream']):
        return False
    if 'Sugar' in selected_allergens and 'sugar' in ingredients_lower:
        return False
    if 'Eggs' in selected_allergens and 'egg' in ingredients_lower:
        return False
    if 'Soy' in selected_allergens and 'soy' in ingredients_lower:
        return False
    return True

# Parse the ingredients input into a list
user_ingredients = [ingredient.strip().lower() for ingredient in ingredients_input.split(',')] if ingredients_input else []

# Filter the dataframe based on the selected categories and ingredient matching
filtered_df = df[df['Category'].isin(categories)]  # Filter recipes by selected categories

# Remove duplicates by recipe title
filtered_df = filtered_df.drop_duplicates(subset=['Recipe Title'])

# Filter recipes based on ingredients and other filters
matched_recipes = []

for index, row in filtered_df.iterrows():
    recipe_ingredients = ' '.join(eval(row['Ingredients'])).lower()
    matched = match_ingredients(recipe_ingredients, user_ingredients)
    
    if not user_ingredients or matched:
        # Apply dietary preference filter
        if filter_dietary_preferences(recipe_ingredients, vegetarian, vegan, gluten_free):
            # Apply allergen filter
            if filter_allergens(recipe_ingredients, selected_allergens):
                matched_recipes.append((row, matched))

# Further filtering based on prep time, cook time, and servings
filtered_recipes = [
    (row, matched) for row, matched in matched_recipes
    if row['Prep Time'] <= prep_time and row['Cook Time'] <= cook_time and row['Servings'] >= servings
]

# Display the filtered list of recipes
st.write(f"Found {len(filtered_recipes)} matching recipes:")

for row, matched in filtered_recipes:
    with st.expander(row['Recipe Title']):
        # Category, Servings, Prep Time, Cook Time
        st.write(f"**Category**: {row['Category']}")
        st.write(f"**Servings**: {int(row['Servings'])}")
        st.write(f"**Prep Time**: {row['Prep Time']} minutes")
        st.write(f"**Cook Time**: {row['Cook Time']} minutes")
        st.write(f"**Total Time**: {row['Total Time']} minutes")

        # Display ingredients as a bullet list
        st.write("### Ingredients")
        ingredients = eval(row['Ingredients'])
        for ingredient in ingredients:
            st.write(f"- {ingredient}")
        
        # Highlight matched ingredients for validation
        if matched:
            st.write(f"**Matched Ingredients**: {', '.join(matched)}")

        # Display instructions as a bullet list (cleaning up the text)
        st.write("### Instructions")
        instructions = eval(row['Instructions'])
        for step in instructions:
            st.write(f"- {step}")
