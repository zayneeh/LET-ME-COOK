import streamlit as st
import pandas as pd
from gtts import gTTS
import os


# Display an image
image_path = 'https://github.com/zayneeh/LET-ME-COOK/blob/main/20241021_212349.jpg'  
st.image(image_path, caption='Nigerian Fried Rice')


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
    user_input = st.text_input('Enter your query:', help='Enter ingredients separated by commas or a food name.')

    if st.button('Find Recipes'):
        if user_input:
            if search_option == 'Ingredients':
                result = get_recipes(user_input)
            else:
                result = get_recipes_by_food_name(user_input)
            if not result.empty:
                recipe_choice = st.selectbox('Select a recipe to listen to:', result['food_name'].tolist())
                selected_recipe = result[result['food_name'] == recipe_choice].iloc[0]
                display_recipe(selected_recipe)
                if st.button('Listen to Recipe'):
                    text_to_speech(selected_recipe)
            else:
                st.write("No recipes found.")
        else:
            st.write("Please enter some input to search for recipes.")

def display_recipe(recipe):
    st.subheader(recipe['food_name'])
    st.write('Ingredients: ' + recipe['ingredients'])
    st.write('Instructions: ' + recipe['procedures'])

def text_to_speech(recipe):
    recipe_text = f"{recipe['food_name']}. Ingredients: {recipe['ingredients']}. Instructions: {recipe['procedures']}"
    tts = gTTS(text=recipe_text, lang='en')
    tts.save('recipe.mp3')
    audio_file = open('recipe.mp3', 'rb')
    audio_bytes = audio_file.read()
    st.audio(audio_bytes, format='audio/mp3', start_time=0)
    os.remove('recipe.mp3')  # Clean up the file after playing

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

