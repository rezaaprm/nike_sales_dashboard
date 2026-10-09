import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Streamlit Web Configuration
st.set_page_config(
    page_title="Video Games Sales Dashboard",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="auto"
)

# Load Dataset
@st.cache_data
def load_data():
    df = pd.read_csv("vgsales.csv")
    df = df.dropna()
    return df

try:
    df = load_data()
except Exception as e:
    st.error(f"Gagal memuat dataset: {e}. Pastikan file 'vgsales.csv' tersedia.")
    st.stop()

# Header Container
st.markdown('<h1 style="text-align: center;">Dashboard of Video Games Sales</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; color: gray;">Exploration Data Analysis on Global Sales</p>', unsafe_allow_html=True)
st.write("---")

# Layout kolom utama
col1, col2 = st.columns(2)

with col1:
    st.subheader("Sum of Games Sales by Regions")
    
    # Ringkasan Penjualan Berdasarkan Region
    region_sales = df[['NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales']].sum().reset_index()
    region_sales.columns = ['Region', 'Sales']
    region_sales['Region'] = region_sales['Region'].str.replace('_Sales', '')
    
    fig_region = px.bar(
        region_sales,
        x='Region',
        y='Sales',
        color='Region',
        title='Total Sales by Region (Million Units)',
        color_discrete_sequence=px.colors.qualitative.Prism
    )
    fig_region.update_layout(
        template="plotly_dark",
        yaxis=dict(rangemode="tozero"),
        showlegend=False
    )
    st.plotly_chart(fig_region, use_container_width=True)

with col2:
    st.subheader("Global Sales Trend Over Time")
    
    # Line chart tren penjualan global per tahun
    yearly_sales = df.groupby('Year')['Global_Sales'].sum().reset_index()
    yearly_sales = yearly_sales[yearly_sales['Year'] <= 2020]
    
    fig_year = px.line(
        yearly_sales,
        x='Year',
        y='Global_Sales',
        markers=True,
        title='Global Sales Trend Over Years',
        labels={'Global_Sales': 'Global Sales (juta unit)', 'Year': 'Year'}
    )
    fig_year.update_layout(
        template="plotly_dark",
        yaxis=dict(rangemode="tozero")
    )
    st.plotly_chart(fig_year, use_container_width=True)

st.write("---")

# --- GRAFIK PENGGANTI BARU: PLOTLY TREEMAP (Hierarki Publisher & Genre) ---
st.subheader("Hierarchical Breakdown: Top Publishers & Genres by Global Sales")
st.markdown("Grafik Interaktif Treemap untuk melihat proporsi penjualan berdasarkan Publisher, Genre, dan Game.")

# Memfilter top publisher agar visualisasi treemap tetap rapi dan tidak terlalu padat
top_publishers = df.groupby('Publisher')['Global_Sales'].sum().reset_index().sort_values(by='Global_Sales', ascending=False).head(15)
df_filtered = df[df['Publisher'].isin(top_publishers['Publisher'])]

fig_treemap = px.treemap(
    df_filtered,
    path=['Publisher', 'Genre', 'Name'],
    values='Global_Sales',
    color='Global_Sales',
    color_continuous_scale='Viridis',
    title='Treemap of Top Publishers and Genres'
)

fig_treemap.update_layout(
    template="plotly_dark",
    margin=dict(t=50, l=25, r=25, b=25)
)

st.plotly_chart(fig_treemap, use_container_width=True)

st.write("---")

# Tampilan Tabel Dataset
st.subheader("Dataset Preview")
st.dataframe(df.head(100), use_container_width=True, hide_index=True)