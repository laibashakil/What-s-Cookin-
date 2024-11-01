import streamlit as st
import pandas as pd
import firebase_admin
from firebase_admin import credentials, firestore
import bcrypt
import matplotlib.pyplot as plt

# Firebase setup
if not firebase_admin._apps:
    # Convert the Streamlit secrets entry to a dictionary
    firebase_credentials = dict(st.secrets["firebase_credentials"])
    cred = credentials.Certificate(firebase_credentials)
    firebase_admin.initialize_app(cred)

# Initialize Firestore
db = firestore.client()


# Load the cleaned dataset (for Recipe Finder)
df = pd.read_csv('cleaned_recipes.csv')

# Function to add a new user to Firestore
def add_user_to_firestore(username, password):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())  # Hash the password
    db.collection('users').document(username).set({
        'username': username,
        'password': hashed_password.decode('utf-8'),  # Store password as a string
        'liked_recipes': []  # Initialize liked recipes list
    })

# Function to validate user login
def login_user(username, password):
    user_ref = db.collection('users').document(username)
    user_doc = user_ref.get()
    if user_doc.exists:
        stored_password = user_doc.to_dict()['password']
        if bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):
            return True
    return False

# Function to fetch liked recipes of a user
def get_liked_recipes(username):
    user_ref = db.collection('users').document(username)
    user_doc = user_ref.get()
    if user_doc.exists:
        return user_doc.to_dict().get('liked_recipes', [])
    return []

# Function to like a recipe
def like_recipe(username, recipe_title):
    user_ref = db.collection('users').document(username)
    user_doc = user_ref.get()
    if user_doc.exists:
        liked_recipes = user_doc.to_dict().get('liked_recipes', [])
        if recipe_title not in liked_recipes:
            liked_recipes.append(recipe_title)
            user_ref.update({'liked_recipes': liked_recipes})
            st.success("❤️ Liked recipe")
        else:
            st.warning("You already liked this recipe.")

# Authentication section
def login_signup_section():
    st.title("Welcome to What's Cookin'!")
    st.markdown("### Please sign up or log in to continue.")
    
    option = st.radio("Choose an option", ["Login", "Sign Up"], horizontal=True)
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        if option == "Login":
            st.subheader("Login")
            username = st.text_input("Username", key="login_username")
            password = st.text_input("Password", type="password", key="login_password")
            if st.button("Login"):
                if login_user(username, password):
                    st.success(f"Welcome back, {username}!")
                    st.session_state['logged_in_user'] = username
                    st.session_state['page'] = 'dashboard'
                    st.rerun()
                else:
                    st.error("Invalid username or password.")
        else:
            st.subheader("Sign Up")
            new_username = st.text_input("New Username", key="signup_username")
            new_password = st.text_input("New Password", type="password", key="signup_password")
            if st.button("Sign Up"):
                if db.collection('users').document(new_username).get().exists:
                    st.warning("This username already exists.")
                else:
                    add_user_to_firestore(new_username, new_password)
                    st.success("Account created successfully! You can now log in.")

# Dashboard section with liked recipes and category pie chart
def render_dashboard(username):
    st.title(f"Welcome to What's Cookin', {username}!")
    
    liked_recipes = get_liked_recipes(username)
    
    # Columns for equal-sized box layout
    col1, col2 = st.columns(2)

    with col1:
        st.header("Liked Recipes")
        if liked_recipes:
            for recipe in liked_recipes:
                recipe_data = df[df['Recipe Title'] == recipe]
                if not recipe_data.empty:
                    recipe_row = recipe_data.iloc[0]
                    with st.expander(recipe_row['Recipe Title']):
                        st.write(f"**Category**: {recipe_row['Category']}")
                        st.write(f"**Servings**: {int(recipe_row['Servings'])}")
                        st.write(f"**Prep Time**: {recipe_row['Prep Time']} minutes")
                        st.write(f"**Cook Time**: {recipe_row['Cook Time']} minutes")
                        st.write(f"**Total Time**: {recipe_row['Total Time']} minutes")
                        st.write("### Ingredients")
                        ingredients = eval(recipe_row['Ingredients'])
                        for ingredient in ingredients:
                            st.write(f"- {ingredient}")
                        st.write("### Instructions")
                        instructions = eval(recipe_row['Instructions'])
                        for step in instructions:
                            st.write(f"- {step}")
        else:
            st.write("You haven't liked any recipes yet.")
    
    with col2:
        if liked_recipes:
            st.header("Category Preferences")
            category_counts = df[df['Recipe Title'].isin(liked_recipes)]['Category'].value_counts()
            fig, ax = plt.subplots(figsize=(4, 4))  # Smaller pie chart
            ax.pie(category_counts, labels=category_counts.index, autopct='%1.1f%%')
            st.pyplot(fig)
        else:
            st.write("No data to display for category preferences.")

# Recipe Finder section
def render_recipe_finder():
    st.title("Recipe Finder")
    st.sidebar.header('Filter Recipes')
    
    categories = st.sidebar.multiselect(
        'Select Category/Categories', 
        df['Category'].unique().tolist(), 
        help="Choose one or more categories"
    )

    ingredients_input = st.sidebar.text_input("Enter ingredients (comma-separated):", "")
    prep_time = st.sidebar.slider("Maximum Prep Time (minutes):", 0, 120, 60)
    cook_time = st.sidebar.slider("Maximum Cook Time (minutes):", 0, 300, 60)
    servings = st.sidebar.slider("Minimum Servings:", 1, 10, 2)

    st.sidebar.header('Dietary Preferences')
    vegetarian = st.sidebar.checkbox("Vegetarian")
    vegan = st.sidebar.checkbox("Vegan")
    gluten_free = st.sidebar.checkbox("Gluten-free")

    allergen_options = ['Peanuts', 'Shellfish', 'Dairy', 'Sugar', 'Eggs', 'Soy']
    selected_allergens = st.sidebar.multiselect("Select allergens to exclude", allergen_options)

    user_ingredients = [ingredient.strip().lower() for ingredient in ingredients_input.split(',')] if ingredients_input else []

    filtered_df = df[df['Category'].isin(categories)] if categories else df
    filtered_df = filtered_df.drop_duplicates(subset=['Recipe Title'])

    matched_recipes = []

    for index, row in filtered_df.iterrows():
        recipe_ingredients = ' '.join(eval(row['Ingredients'])).lower()
        if not user_ingredients or any(ingredient in recipe_ingredients for ingredient in user_ingredients):
            matched_recipes.append(row)

    filtered_recipes = [
        row for row in matched_recipes
        if row['Prep Time'] <= prep_time and row['Cook Time'] <= cook_time and row['Servings'] >= servings
    ]

    st.write(f"Found {len(filtered_recipes)} matching recipes:")

    for row in filtered_recipes:
        with st.expander(row['Recipe Title']):
            st.write(f"**Category**: {row['Category']}")
            st.write(f"**Servings**: {int(row['Servings'])}")
            st.write(f"**Prep Time**: {row['Prep Time']} minutes")
            st.write(f"**Cook Time**: {row['Cook Time']} minutes")
            st.write(f"**Total Time**: {row['Total Time']} minutes")
            st.write("### Ingredients")
            ingredients = eval(row['Ingredients'])
            for ingredient in ingredients:
                st.write(f"- {ingredient}")
            st.write("### Instructions")
            instructions = eval(row['Instructions'])
            for step in instructions:
                st.write(f"- {step}")

            # Like button with heart icon
            if st.button("❤️ Like Recipe", key=f"like_{row['Recipe Title']}"):
                if 'logged_in_user' in st.session_state:
                    like_recipe(st.session_state['logged_in_user'], row['Recipe Title'])
                else:
                    st.error("You must be logged in to like a recipe.")

# Sidebar navigation with sign out option
def render_sidebar():
    st.sidebar.title("Navigation")
    selection = st.sidebar.radio("Go to", ["Home", "Recipe Finder"])
    if st.sidebar.button("Sign Out"):
        del st.session_state['logged_in_user']
        st.session_state['page'] = 'login'
        st.rerun()
    return selection

# Main logic for routing
if 'page' not in st.session_state:
    st.session_state['page'] = 'login'

if st.session_state['page'] == 'login':
    login_signup_section()
elif st.session_state['page'] == 'dashboard':
    if 'logged_in_user' in st.session_state:
        selection = render_sidebar()
        if selection == "Home":
            render_dashboard(st.session_state['logged_in_user'])
        elif selection == "Recipe Finder":
            render_recipe_finder()
    else:
        st.error("You are not logged in. Please log in to continue.")
        st.session_state['page'] = 'login'
        st.rerun()
