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


top_5_reviews = df.sort_values(by='reviews', ascending=False).head(5)

fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(y='product_name', x='reviews', data=top_5_reviews, palette='cividis', ax=ax)
ax.set_title('Top 5 Products with The Most Reviews', fontsize=15)
ax.set_xlabel('Product Name', fontsize=12)
ax.set_ylabel('Review', fontsize=12)
ax.tick_params(axis='x', rotation=90)

plt.tight_layout()
st.pyplot(fig)
# plt.show()



top_5_listing_price = df.sort_values(by='listing_price', ascending=False).head(5)

fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(y='product_name', x='listing_price', data=top_5_listing_price, palette='plasma', ax=ax)

ax.set_title('Top 5 Products with Highest Listing Price', fontsize=15)
ax.set_xlabel('Listing Price', fontsize=12)
ax.set_ylabel('Product Name', fontsize=12)
ax.tick_params(axis='y')

plt.tight_layout()
st.pyplot(fig)
# plt.show()



top_price_amount = df.sort_values(by='sale_price', ascending=False).head(100)

fig, ax = plt.subplots(figsize=(8, 4))
sns.countplot(data=top_price_amount, x="sale_price", palette="viridis", ax=ax)

ax.set_title("Count of Top Prices Amount", fontsize=14)
ax.set_xlabel("Price", fontsize=14)
ax.set_ylabel("Count", fontsize=14)
ax.grid(axis='y')

plt.tight_layout()
st.pyplot(fig)
# plt.show()



df3 = df[df['reviews'] == 9]
filtered_df3 = df[df['rating'] == 5.0][["product_name", "sale_price", "rating", "reviews"]].sort_values("reviews", ascending=False)
top_5_reviews = filtered_df3.sort_values(by="reviews", ascending=False).head(10)

melted_df = top_5_reviews.melt(id_vars="product_name", value_vars=["rating", "reviews"], var_name="Metric", value_name="Value")
df_new = melted_df.pivot_table(index="product_name", columns="Metric", values="Value", aggfunc="sum")

fig, ax = plt.subplots(figsize=(10, 6))
df_new.plot(kind="bar", stacked=True, ax=ax, colormap="vlag")

ax.set_title("Comparison of Ratings and Reviews for Top 5 Products", fontsize=16)
ax.set_xlabel("Product Name", fontsize=12)
ax.set_ylabel("Rating / Review", fontsize=12)
ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
plt.tight_layout()
st.pyplot(fig)
# plt.show()