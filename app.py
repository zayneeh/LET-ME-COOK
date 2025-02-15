import streamlit as st
import pandas as pd

# URL to the raw image content on GitHub
image_url = 'https://raw.githubusercontent.com/zayneeh/LET-ME-COOK/main/20241021_212349.jpg'

# Display the image in Streamlit
st.image(image_url, caption='Nigerian Fried Rice', width =150)


# Load the CSV data into a DataFrame
@st.cache_data  # This decorator caches the data to prevent reloading on every interaction
def load_data(filename):
    data = pd.read_csv(filename)
    data.columns = [col.strip().lower() for col in data.columns] 
    return data

recipes = load_data('Nigerian Palatable meals - Sheet1.csv')

# Function to filter recipes based on ingredients
def get_recipes(ingredients):
    ingredients = [ingredient.strip().lower() for ingredient in ingredients.split(',')]
    filtered_recipes = recipes[recipes['ingredients'].apply(lambda x: all(ingredient in x.lower() for ingredient in ingredients))]
    return filtered_recipes
    
#Function to filter recipes based on food-name
def get_recipes_by_food_name(food_name):
    food_name = [food_name.strip().lower() for food in food_name.split(',')]
    filtered_recipes = recipes[recipes['food_name'].apply(lambda x: all(food in x.lower() for food in food_name))]
    return filtered_recipes

# Streamlit interface
def main():
    st.title('LET ME COOK')
    st.header('Discover Delicious Nigerian Recipes')

    search_option = st.radio("Search by:", ('Ingredients', 'Food Name'))

    if search_option == 'Ingredients':
        user_input = st.text_input('Enter your ingredients, separated by commas:')
        if st.button('Find Recipes by Ingredients'):
            if user_input:
                result = get_recipes(user_input)
                display_recipes(result)
            else:
                st.write("Please enter some ingredients to search for recipes.")
    elif search_option == 'Food Name':
        user_input = st.text_input('Enter a food name:')
        if st.button('Find Recipes by Food Name'):
            if user_input:
                result = get_recipes_by_food_name(user_input)
                display_recipes(result)
            else:
                st.write("Please enter a food name to search for recipes.")

        
def display_recipes(recipes):
    if recipes.empty:
        st.write("No recipes found.")
    else:
        for index, row in recipes.iterrows():
            st.subheader(row['food_name'])
            st.write('Ingredients: ' + row['ingredients'])
            st.write('Instructions: ' + row['procedures'])



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


