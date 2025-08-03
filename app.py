import streamlit as st
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import warnings

warnings.filterwarnings("ignore", category=FutureWarning)

# Show image
image_url = 'https://raw.githubusercontent.com/zayneeh/LET-ME-COOK/main/20241021_212349.jpg'
st.image(image_url, caption='Nigerian Fried Rice', width=150)

# Load data
@st.cache_data
def load_data(filename):
    df = pd.read_csv(filename)
    df.columns = [col.strip().lower() for col in df.columns]
    # Combine fields for better prompt matching
    df["combined"] = df["food_name"].fillna('') + ", " + \
                     df["ingredients"].fillna('').str.replace("\r\n", ", ") + ", " + \
                     df["procedures"].fillna('')
    df["combined"] = df["combined"].str.lower()
    return df

recipes_df = load_data('Nigerian Palatable meals - Sheet1.csv')

# Cache model and embeddings
@st.cache_data
def get_embeddings(df):
    model = SentenceTransformer("paraphrase-MiniLM-L3-v2")
    embeddings = model.encode(df["combined"].tolist())
    return embeddings, model

recipe_embeddings, model = get_embeddings(recipes_df)

# Semantic recommendation (prompt/ingredient match)
def semantic_recipe_recommendation(user_input, embeddings, threshold=0.7):
    user_vec = model.encode([user_input.strip().lower()])[0]
    similarities = cosine_similarity([user_vec], embeddings)[0]
    matches = [(i, sim) for i, sim in enumerate(similarities) if sim >= threshold]
    results = recipes_df.iloc[[i for i, _ in matches]]
    return results.sort_values(by='food_name')

# Food name match
def get_recipes_by_food_name(food_name):
    food_name = [f.strip().lower() for f in food_name.split(',')]
    return recipes_df[recipes_df['food_name'].apply(lambda x: all(f in x.lower() for f in food_name))]

# Display results
def display_recipes(recipes):
    if recipes.empty:
        st.write("No recipes found.")
    else:
        for _, row in recipes.iterrows():
            st.subheader(row['food_name'])
            st.write('Ingredients: ' + row['ingredients'])
            st.write('Instructions: ' + row['procedures'])
            st.markdown('---')

# UI
def main():
    st.title('LET ME COOK')
    st.header('Discover Delicious Nigerian Recipes')

    search_option = st.radio("Search by:", ('Ingredients', 'Food Name', 'Prompt/Description'))

    if search_option == 'Ingredients':
        st.caption("Type a list of ingredients separated by commas. For example: rice, tomato, pepper, onions")
        user_input = st.text_input('Enter ingredients')
        if st.button('Find Recipes by Ingredients'):
            if user_input:
                with st.spinner("Searching..."):
                    result = semantic_recipe_recommendation(user_input, recipe_embeddings)
                display_recipes(result)
            else:
                st.warning("Please enter some ingredients.")

    elif search_option == 'Food Name':
        user_input = st.text_input('Enter a food name (e.g., "Jollof Rice")')
        if st.button('Find Recipes by Food Name'):
            if user_input:
                result = get_recipes_by_food_name(user_input)
                display_recipes(result)
            else:
                st.warning("Please enter a food name.")

    elif search_option == 'Prompt/Description':
        user_input = st.text_input('Describe what you want (e.g., "spicy rice dish with chicken")')
        if st.button('Find Recipes from Prompt'):
            if user_input:
                with st.spinner("Matching your prompt..."):
                    result = semantic_recipe_recommendation(user_input, recipe_embeddings)
                display_recipes(result)
            else:
                st.warning("Please enter a prompt or description.")

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





