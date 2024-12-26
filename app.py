import streamlit as st
import pandas as pd


# Load the CSV data into a DataFrame
@st.cache_data  # This decorator caches the data to prevent reloading on every interaction
def load_data(filename):
    data = pd.read_csv(filename)
    data.columns = [col.strip().lower() for col in data.columns] 
    return data

recipes = load_data('C:\\Users\\HP\\Desktop\\SAMPLE\\LET ME COOK\\Nigerian Palatable meals.csv')

# Function to filter recipes based on ingredients
def get_recipes(ingredients):
    ingredients = [ingredient.strip().lower() for ingredient in ingredients.split(',')]
    filtered_recipes = recipes[recipes['ingredients'].apply(lambda x: all(ingredient in x.lower() for ingredient in ingredients))]
    return filtered_recipes

# Streamlit interface
def main():
    st.title('LET ME COOK')
    st.header('Discover Delicious Nigerian Recipes')
    
    # User inputs their ingredients
    user_ingredients = st.text_input("Let's find what you can cook!Enter the ingredients you have separated by commas:")
    
    if st.button('Find Recipes'):
        if user_ingredients:
            result = get_recipes(user_ingredients)
            if not result.empty:
                for index, row in result.iterrows():
                    st.subheader(row['food_name'])  # Recipe name
                    st.text('Ingredients: ' + row['ingredients'])
                    st.text('Instructions: ' + row['procedures'])
            else:
                st.write("No recipes found that match the given ingredients.")
        else:
            st.write("Please enter some ingredients to search for recipes.")

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

