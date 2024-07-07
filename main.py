import streamlit as st
import pandas as pd
from PIL import Image
import os
from transformers import AutoTokenizer, TFAutoModelForSequenceClassification

# Initialize the tokenizer and model
tokenizer = AutoTokenizer.from_pretrained("ilsilfverskiold/tech-keywords-extractor")
model = TFAutoModelForSequenceClassification.from_pretrained("ilsilfverskiold/tech-keywords-extractor")

# Load dataset (replace with your actual dataset)
df = pd.read_csv("styles.csv")

# Define a function to parse the query and extract keywords
def parse_query(query):
    inputs = tokenizer(query, return_tensors="pt", max_length=512, truncation=True)
    outputs = model.generate(**inputs)
    result = tokenizer.decode(outputs[0], skip_special_tokens=True)
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

# Function to display filtered products in a grid layout
def display_results(filtered_products):
    if filtered_products.empty:
        st.write("No products found.")
    else:
        num_items = len(filtered_products)
        items_per_row = 3
        num_rows = (num_items - 1) // items_per_row + 1

        for i in range(num_rows):
            row_items = filtered_products.iloc[i * items_per_row:(i + 1) * items_per_row]
            row_container = st.container()  # Container for each row
            with row_container:
                st.write("<div style='display:flex; flex-wrap: wrap;'>", unsafe_allow_html=True)
                for index, row in row_items.iterrows():
                    st.write("<div style='border: 1px solid black; padding: 10px; margin: 10px; flex: 1; max-width: 30%; box-sizing: border-box;'>", unsafe_allow_html=True)
                    st.write(f"**Product ID:** {row['id']}")
                    st.write(f"**Product Name:** {row['productDisplayName']}")
                    st.write(f"**Base Colour:** {row['baseColour']}")
                    st.write(f"**Price:** {row['price'] if 'price' in row else 'N/A'}")
                    image_path = os.path.join("images", f"{row['id']}.jpg")
                    if os.path.exists(image_path):
                        image = Image.open(image_path)
                        st.image(image, caption=row['productDisplayName'], width=150)
                    st.write("</div>", unsafe_allow_html=True)
                st.write("</div>", unsafe_allow_html=True)

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
    }
    /* Custom styling for text input */
    .stTextInput input {
        border: 2px solid #931820 !important;
        border-radius: 10px !important;
        padding: 8px 12px !important;
        font-size: 16px !important;
        color: #931820 !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.header("Vastr:red[Ai]", divider='rainbow')
st.warning("If you get any error, try reloading the website :)")

# Sidebar
st.sidebar.subheader("Model Information")
st.sidebar.write("""
- **Model:** VastrAi
- **Description:** Recommends fashion items based on user input.
- **Version:** 1.1.0
""")

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
        display_results(filtered_products)

    if st.button("Find me a winter jacket"):
        query = "Find me a winter jacket"
        keywords = parse_query(query)
        filtered_products = filter_products(df, keywords)
        display_results(filtered_products)

    if st.button("Suggest a casual outfit"):
        query = "Suggest a casual outfit"
        keywords = parse_query(query)
        filtered_products = filter_products(df, keywords)
        display_results(filtered_products)

    if st.button("Recommend some formal wear"):
        query = "Recommend some formal wear"
        keywords = parse_query(query)
        filtered_products = filter_products(df, keywords)
        display_results(filtered_products)
