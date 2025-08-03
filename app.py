import streamlit as st
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# URL to the raw image content on GitHub
image_url = 'https://raw.githubusercontent.com/zayneeh/LET-ME-COOK/main/20241021_212349.jpg'

# Display the image in Streamlit
st.image(image_url, caption='Nigerian Fried Rice', width=150)

# Load the CSV data into a DataFrame
@st.cache_data
def load_data(filename):
    data = pd.read_csv(filename)
    data.columns = [col.strip().lower() for col in data.columns]
    data['combined_text'] = data['ingredients'] + ' ' + data['procedures']
    return data

# Load embeddings
@st.cache_data
def load_embeddings(text_data):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embeddings = model.encode(text_data.tolist())
    return model, embeddings

recipes = load_data('Nigerian Palatable meals - Sheet1.csv')
model, recipe_embeddings = load_embeddings(recipes['combined_text'])

# Function to recommend recipes based on semantic similarity
def recommend_recipes(user_input, model, embeddings, df, top_k=5):
    user_embedding = model.encode([user_input])[0]
    similarities = cosine_similarity([user_embedding], embeddings)[0]
    top_indices = similarities.argsort()[-top_k:][::-1]
    return df.iloc[top_indices], similarities[top_indices]

# Function to display recommended recipes
def display_recipes(recipes):
    if recipes.empty:
        st.write("No recipes found.")
    else:
        for index, row in recipes.iterrows():
            st.subheader(row['food_name'])
            st.write('Ingredients: ' + row['ingredients'])
            st.write('Instructions: ' + row['procedures'])
            st.markdown('---')

# Streamlit interface
def main():
    st.title('LET ME COOK')
    st.header('Discover Delicious Nigerian Recipes')

    user_input = st.text_input('Describe what you want to eat (e.g., "spicy rice with vegetables")')
    if st.button('Recommend Recipes'):
        if user_input:
            recommended, scores = recommend_recipes(user_input, model, recipe_embeddings, recipes)
            display_recipes(recommended)
        else:
            st.write("Please enter a description to get recommendations.")

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



