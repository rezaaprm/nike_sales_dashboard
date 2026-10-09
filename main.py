# Streamlit
import streamlit as st
import warnings

from streamlit_extras.add_vertical_space import add_vertical_space

# Main Library
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Streamlit Web Configuration
st.set_page_config(
    page_title="My Dashboard - Nike",
    page_icon="",
    layout="wide",
    initial_sidebar_state="auto"
)

dataset = pd.read_csv("nike_shoes_sales.csv")
df = dataset.ffill().drop('discount', axis=1)

# Container - Header
with st.container(border=False):
    st.markdown('<h1 style=text-align:center>My Nike Dashboard - Created by M Reza A P</h1>', unsafe_allow_html=True)
    add_vertical_space(3)

st.success("Nike Dataset")
st.dataframe(data=df, width=1500, use_container_width=True, hide_index=True)


# --- Grafik 1: Top 5 Products by Reviews ---
top_5_reviews = df.sort_values(by='reviews', ascending=False).head(5)

fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(y='product_name', x='reviews', data=top_5_reviews, palette='cividis', ax=ax)
ax.set_title('Top 5 Products with The Most Reviews', fontsize=15)
ax.set_xlabel('Review Count', fontsize=12)
ax.set_ylabel('Product Name', fontsize=12)

plt.tight_layout()
st.pyplot(fig)


# --- Grafik 2: Top 5 Products by Listing Price ---
top_5_listing_price = df.sort_values(by='listing_price', ascending=False).head(5)

fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(y='product_name', x='listing_price', data=top_5_listing_price, palette='plasma', ax=ax)

ax.set_title('Top 5 Products with Highest Listing Price', fontsize=15)
ax.set_xlabel('Listing Price', fontsize=12)
ax.set_ylabel('Product Name', fontsize=12)

plt.tight_layout()
st.pyplot(fig)


# --- Grafik 3: Distribution of Top Sale Prices (Diperbaiki menggunakan histplot) ---
top_price_amount = df.sort_values(by='sale_price', ascending=False).head(100)

fig, ax = plt.subplots(figsize=(10, 5))
sns.histplot(data=top_price_amount, x="sale_price", kde=True, color="teal", ax=ax)

ax.set_title("Distribution of Top Sale Prices", fontsize=14)
ax.set_xlabel("Sale Price", fontsize=14)
ax.set_ylabel("Frequency", fontsize=14)
ax.grid(axis='y', linestyle='--', alpha=0.7)

plt.tight_layout()
st.pyplot(fig)


# --- Grafik 4: Top Reviews for 5.0 Rated Products (Diperbaiki dari Stacked Chart yang Salah Skala) ---
top_rated_products = df[df['rating'] == 5.0].sort_values(by="reviews", ascending=False).head(10)

fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(y='product_name', x='reviews', data=top_rated_products, palette='viridis', ax=ax)

ax.set_title("Top Reviews for 5.0 Rated Products", fontsize=16)
ax.set_xlabel("Review Count", fontsize=12)
ax.set_ylabel("Product Name", fontsize=12)

plt.tight_layout()
st.pyplot(fig)