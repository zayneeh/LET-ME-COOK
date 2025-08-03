import streamlit as st
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import warnings

# Suppress future warnings
warnings.filterwarnings("ignore", category=FutureWarning)

# Show header image
image_url = 'https://raw.githubusercontent.com/zayneeh/LET-ME-COOK/main/20241021_212349.jpg'
st.image(image_url, caption='Nigerian Fried Rice', width=150)

# Load CSV file
@st.cache_data
def load_data(filename):
    data = pd.read_csv(filename)
    data.columns = [col.strip().lower() for col in data.columns]
    return data

recipes_df = load_data('Nigerian Palatable meals - Sheet1.csv')

# Load sentence-transformer model
@st.cache_resource
def load_model():
    return SentenceTransformer("paraphrase-MiniLM-L3-v2")

model = load_model()

# Cache recipe embeddings
@st.cache_data
def get_recipe_embeddings(df, model):
    ingredient_texts = df['ingredients'].str.replace("\r\n", ", ").str.lower().tolist()
    embeddings = model.encode(ingredient_texts)
    return embeddings

recipe_embeddings = get_recipe_embeddings(recipes_df, model)

# Semantic recommendation
def semantic_recipe_recommendation(user_input, df, recipe_embeddings, threshold=0.7):
    user_vec = model.encode([user_input.strip().lower()])[0]
    similarities = cosine_similarity([user_vec], recipe_embeddings)[0]
    matches = [(i, sim) for i, sim in enumerate(similarities) if sim >= threshold]
    results = df.iloc[[i for i, _ in matches]]
    return results.sort_values(by='food_name')

# Food name matching
def get_recipes_by_food_name(food_name):
    food_name = [f.strip().lower() for f in food_name.split(',')]
    return recipes_df[recipes_df['food_name'].apply(lambda x: all(f in x.lower() for f in food_name))]

# Display recipes
def display_recipes(recipes):
    if recipes.empty:
        st.write("No recipes found.")
    else:
        for _, row in recipes.iterrows():
            st.subheader(row['food_name'])
            st.write('Ingredients: ' + row['ingredients'])
            st.write('Instructions: ' + row['procedures'])
            st.markdown('---')

# Streamlit interface
def main():
    st.title('LET ME COOK')
    st.header('Discover Delicious Nigerian Recipes')

    search_option = st.radio("Search by:", ('Ingredients', 'Food Name', 'Prompt/Description'))

    if search_option == 'Ingredients':
        user_input = st.text_input('Enter ingredients (e.g., "rice, tomato, pepper")')
        if st.button('Find Recipes by Ingredients'):
            if user_input:
                with st.spinner("Searching for recipes..."):
                    result = semantic_recipe_recommendation(user_input, recipes_df, recipe_embeddings)
                display_recipes(result)
            else:
                st.write("Please enter some ingredients.")
    elif search_option == 'Food Name':
        user_input = st.text_input('Enter a food name (e.g., "Fried Rice")')
        if st.button('Find Recipes by Food Name'):
            if user_input:
                result = get_recipes_by_food_name(user_input)
                display_recipes(result)
            else:
                st.write("Please enter a food name.")
    elif search_option == 'Prompt/Description':
        user_input = st.text_input('Describe what you want (e.g., "a spicy rice dish with vegetables")')
        if st.button('Find Recipes from Prompt'):
            if user_input:
                with st.spinner("Finding matches..."):
                    result = semantic_recipe_recommendation(user_input, recipes_df, recipe_embeddings)
                display_recipes(result)
            else:
                st.write("Please enter a description or prompt.")

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



