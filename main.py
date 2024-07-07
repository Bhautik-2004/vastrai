import streamlit as st
import pandas as pd
from PIL import Image
import os
from transformers import pipeline



# Initialize the keyword extraction pipeline
pipe = pipeline("text2text-generation", model="ilsilfverskiold/tech-keywords-extractor")

# Load dataset
df = pd.read_csv("styles.csv")

# Define a function to parse the query and extract keywords
def parse_query(query):
    result = pipe(query)[0]['generated_text']
    keywords = result.split(', ')
    st.write(f"**Extracted Keywords:** {keywords}")  # Debugging line to check extracted keywords
    return keywords

# Function to filter the dataset based on any of the keywords
def filter_products(df, keywords):
    mask = pd.Series([False] * len(df))
    for keyword in keywords:
        keyword = keyword.strip()
        if keyword:
            sub_keywords = keyword.split()
            sub_masks = []
            for sub_keyword in sub_keywords:
                sub_masks.append(df['masterCategory'].str.contains(sub_keyword, case=False, na=False) | \
                                 df['subCategory'].str.contains(sub_keyword, case=False, na=False) | \
                                 df['articleType'].str.contains(sub_keyword, case=False, na=False) | \
                                 df['baseColour'].str.contains(sub_keyword, case=False, na=False) | \
                                 df['season'].str.contains(sub_keyword, case=False, na=False) | \
                                 df['usage'].str.contains(sub_keyword, case=False, na=False) | \
                                 df['gender'].str.contains(sub_keyword, case=False, na=False))
            sub_mask_df = pd.DataFrame(sub_masks).transpose()
            mask = mask | sub_mask_df.any(axis=1)
    return df[mask]

# Function to display filtered products
def display_results(filtered_products):
    if filtered_products.empty:
        st.write("No products found.")
    else:
        for index, row in filtered_products.head(10).iterrows():  # Limit to top 10 items
            st.write(f"**Product ID:** {row['id']}")
            st.write(f"**Product Name:** {row['productDisplayName']}")
            st.write(f"**Base Colour:** {row['baseColour']}")
            st.write(f"**Price:** {row['price'] if 'price' in row else 'N/A'}")
            image_path = os.path.join("images",
                                      f"{row['id']}.jpg")  # Assuming image filenames are the same as product IDs
            if os.path.exists(image_path):
                image = Image.open(image_path)
                st.image(image, caption=row['productDisplayName'])
            st.write("---")

# Streamlit app
st.set_page_config(layout="wide")

# Custom CSS for styling
st.markdown("""
    <style>
    .css-1aumxhk {
        padding-top: 2rem;
    }
    .css-18e3th9 {
        padding-top: 0.5rem;
        padding-bottom: 0.5rem;
        padding-left: 1rem;
        padding-right: 1rem;
        background-color: #ffffff;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    .stButton button {
        border-color: #931820;
        background-color: #931820;
        color: white;
        border-radius: 21px;
    }
    .stButton button:hover {
        border-color: #460b0f;
        background-color: #460b0f;
        color: white;
    }
    .css-2trqyj {
        margin-bottom: 2rem;
    }
    .css-1v0mbdj, .css-1cpxqw2 {
        color: black !important;
    }
    .css-2sbaz0 {
        border: 1px solid black !important;
        color: white !important;
    }
    .css-10trblm h1 {
        color: black !important;
    }
    /* Custom styling for warning message */
    .stWarning {
        color: red !important;
        font-size: 18px !important;
        font-weight: bold !important;
        border-radius: 21px;
    }
    /* Custom styling for text input */
    .stTextInput input {
        border-radius: 21px !important;
        padding: 8px 12px !important;
        font-size: 16px !important;
        color: #931820 !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.header("Vastr:red[Ai]", divider='rainbow')
st.warning("⚠️ If you get any error, try reloading the website :)")
st.warning("⚠️ Somtimes, you won't get relevant recommendations")

# Sidebar
st.sidebar.header("Vastr:red[Ai] ✨")
st.sidebar.subheader("Model Information")
st.sidebar.write("""
- **Model:** VastrAi
- **Description:** Recommends fashion items based on user input.
- **Version:** 1.1.0
- **Developer:** Bhautik Vaghamshi
""")
st.sidebar.page_link("https://www.instagram.com/bhautikvaghamshi/", label="My Instagram Profile")
st.sidebar.page_link("https://www.linkedin.com/in/bhautik-vaghamshi-858a0b1b2/", label="My LinkedIn Profile")

st.sidebar.subheader("Recommendations")

# Main section
main_column, _ = st.columns([2, 1])

with main_column:
    st.subheader("Enter your fashion query below:")
    query = st.text_input("Enter your query here...")

    if st.button("Recommend"):
        keywords = parse_query(query)
        st.write(f"**Extracted Keywords:** {keywords}")  # Debugging line to check extracted keywords
        filtered_products = filter_products(df, keywords)
        display_results(filtered_products)

# Sidebar buttons
with st.sidebar:
    if st.button("Show me summer clothes"):
        query = "Show me summer clothes"
        keywords = parse_query(query)
        filtered_products = filter_products(df, keywords)
        with main_column:
            display_results(filtered_products)

    if st.button("Find me a winter jacket"):
        query = "Find me a winter jacket"
        keywords = parse_query(query)
        filtered_products = filter_products(df, keywords)
        with main_column:
            display_results(filtered_products)

    if st.button("Suggest a casual outfit"):
        query = "Suggest a casual outfit"
        keywords = parse_query(query)
        filtered_products = filter_products(df, keywords)
        with main_column:
            display_results(filtered_products)

    if st.button("Recommend some formal wear"):
        query = "Recommend some formal wear"
        keywords = parse_query(query)
        filtered_products = filter_products(df, keywords)
        with main_column:
            display_results(filtered_products)
