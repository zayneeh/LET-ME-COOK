import streamlit as st
import pandas as pd

# Image display
image_url = 'https://raw.githubusercontent.com/zayneeh/LET-ME-COOK/main/20241021_212349.jpg'
st.image(image_url, caption='Nigerian Fried Rice', width=150)

# Load the CSV data into a DataFrame
@st.cache_data
def load_data(filename):
    data = pd.read_csv(filename)
    data.columns = [col.strip().lower() for col in data.columns]
    return data

recipes = load_data('Nigerian Palatable meals - Sheet1.csv')

# Function to recommend recipes based on ~90% ingredient match
def get_recipes_by_ingredients(user_ingredients):
    user_ingredients = [ingredient.strip().lower() for ingredient in user_ingredients.split(',')]
    results = []

    for idx, row in recipes.iterrows():
        recipe_ingredients = [i.strip().lower() for i in row['ingredients'].split(',')]
        matched = [ing for ing in user_ingredients if ing in recipe_ingredients]

        if len(user_ingredients) == 0:
            continue

        match_ratio = len(matched) / len(user_ingredients)

        if match_ratio >= 0.7:
            results.append(row)

    return pd.DataFrame(results)

# Function to search by food name
def get_recipes_by_food_name(food_name):
    food_name = [f.strip().lower() for f in food_name.split(',')]
    return recipes[recipes['food_name'].apply(lambda x: all(f in x.lower() for f in food_name))]

# Display recipes
def display_recipes(recipes):
    if recipes.empty:
        st.write("No recipes found.")
    else:
        for index, row in recipes.iterrows():
            st.subheader(row['food_name'])
            st.write('Ingredients: ' + row['ingredients'])
            st.write('Instructions: ' + row['procedures'])
            st.markdown('---')

# Streamlit UI
def main():
    st.title('LET ME COOK')
    st.header('Discover Delicious Nigerian Recipes')

    search_option = st.radio("Search by:", ('Ingredients', 'Food Name'))

    if search_option == 'Ingredients':
        user_input = st.text_input('Enter your ingredients, separated by commas:')
        if st.button('Find Recipes by Ingredients'):
            if user_input:
                result = get_recipes_by_ingredients(user_input)
                display_recipes(result)
            else:
                st.write("Please enter some ingredients.")
    elif search_option == 'Food Name':
        user_input = st.text_input('Enter a food name:')
        if st.button('Find Recipes by Food Name'):
            if user_input:
                result = get_recipes_by_food_name(user_input)
                display_recipes(result)
            else:
                st.write("Please enter a food name.")

# Styling
st.markdown("""
<style>
    .stButton>button {
        color: white;
        background-color: #f63366;
        border-radius: 10px;
        border: 2px solid #f63366;
        padding: 10px 24px;
        font-size: 16px;
    }
    .stTextInput>input {
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

if __name__ == "__main__":
    main()

# Footer
st.markdown("""
<style>
    .footer {
        font-size:12px;
        color: #b0b6c1;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="footer">Made with ❤️ by Zainab</p>', unsafe_allow_html=True)
