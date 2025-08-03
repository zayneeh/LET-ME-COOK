import streamlit as st
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import re

# Load image
image_url = 'https://raw.githubusercontent.com/zayneeh/LET-ME-COOK/main/20241021_212349.jpg'
st.image(image_url, caption='Nigerian Fried Rice', width=150)

# Load dataset
@st.cache_data
def load_data(filename):
    df = pd.read_csv(filename)
    df.columns = [col.strip().lower() for col in df.columns]
    df['combined'] = df['food_name'].fillna('') + ', ' + \
                     df['ingredients'].fillna('').str.replace("\r\n", ', ') + ', ' + \
                     df['procedures'].fillna('')
    df['combined'] = df['combined'].str.lower()
    return df

recipes_df = load_data('Nigerian Palatable meals - Sheet1.csv')

# Load model and embeddings
@st.cache_data
def load_embeddings(df):
    model = SentenceTransformer('paraphrase-MiniLM-L3-v2')
    embeddings = model.encode(df['combined'].tolist())
    return embeddings, model

recipe_embeddings, model = load_embeddings(recipes_df)

# 70% ingredient overlap logic
def ingredient_match_70(user_input, df, threshold=0.7):
    user_ingredients = [i.strip().lower() for i in user_input.split(',') if i.strip()]
    matched_rows = []

    for _, row in df.iterrows():
        recipe_ings = re.split(r'[,\\n\\r]', row['ingredients'].lower())
        recipe_ings = [i.strip() for i in recipe_ings if i.strip()]
        matches = [i for i in user_ingredients if i in recipe_ings]

        if len(user_ingredients) == 0:
            continue

        match_ratio = len(matches) / len(user_ingredients)
        if match_ratio >= threshold:
            matched_rows.append(row)

    return pd.DataFrame(matched_rows)

# Semantic prompt matching (conversational)
def semantic_prompt_match(prompt, df, embeddings, threshold=0.6):
    prompt_vec = model.encode([prompt.strip().lower()])[0]
    scores = cosine_similarity([prompt_vec], embeddings)[0]
    matches = [(i, score) for i, score in enumerate(scores) if score >= threshold]
    return df.iloc[[i for i, _ in matches]].sort_values(by='food_name')

# Food name exact match
def get_recipes_by_food_name(food_name):
    food_name = [f.strip().lower() for f in food_name.split(',')]
    return recipes_df[recipes_df['food_name'].apply(lambda x: all(f in x.lower() for f in food_name))]

# Display
def display_recipes(recipes):
    if recipes.empty:
        st.write("No recipes found.")
    else:
        for _, row in recipes.iterrows():
            st.subheader(row['food_name'])
            st.write('**Ingredients:** ' + row['ingredients'])
            st.write('**Instructions:** ' + row['procedures'])
            st.markdown('---')

# Streamlit UI
def main():
    st.title('LET ME COOK')
    st.header('Discover Delicious Nigerian Recipes')

    search_option = st.radio("How do you want to search?", ('By Ingredients', 'By Food Name', 'Talk to Me'))

    if search_option == 'By Ingredients':
        st.caption("Type a list of ingredients separated by commas. For example: rice, tomato, pepper, onions")
        user_input = st.text_input("Ingredients")
        if st.button("Find Recipes by Ingredients"):
            if user_input:
                with st.spinner("Matching by ingredients..."):
                    result = ingredient_match_70(user_input, recipes_df)
                display_recipes(result)
            else:
                st.warning("Please enter at least one ingredient.")

    elif search_option == 'By Food Name':
        user_input = st.text_input("Enter food name (e.g., Jollof Rice)")
        if st.button("Find Recipes by Name"):
            if user_input:
                result = get_recipes_by_food_name(user_input)
                display_recipes(result)
            else:
                st.warning("Please enter a food name.")

    elif search_option == 'Talk to Me':
        st.caption("Ask me anything. For example: What can I make with just turkey and rice?")
        user_input = st.text_input("Ask a question or describe what you want")
        if st.button("Get Suggestions"):
            if user_input:
                with st.spinner("Thinking..."):
                    result = semantic_prompt_match(user_input, recipes_df, recipe_embeddings)
                display_recipes(result)
            else:
                st.warning("Please enter a question or prompt.")

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






