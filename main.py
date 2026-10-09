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
    # Pastikan file vgsales.csv berada di direktori yang sama
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
    st.subheader("Sales by Platform and Region")
    
    # PERBAIKAN: Mengganti Stacked Bar ber-arsiran dengan Grouped Bar Chart Plotly yang bersih
    platform_region_sales = df.groupby('Platform')[['NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales']].sum().reset_index()
    top_platforms = platform_region_sales.sort_values(by='NA_Sales', ascending=False).head(5)
    
    melted_df = top_platforms.melt(
        id_vars='Platform', 
        value_vars=['NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales'],
        var_name='Region', 
        value_name='Sales'
    )
    
    # Membersihkan nama region agar lebih rapi saat ditampilkan
    melted_df['Region'] = melted_df['Region'].str.replace('_Sales', '')
    
    fig_platform = px.bar(
        melted_df,
        x='Platform',
        y='Sales',
        color='Region',
        barmode='group', # Berkelompok (grouped) agar mudah dibandingkan tanpa arsiran rumit
        title='Top Platforms Sales by Region',
        labels={'Sales': 'Jumlah Penjualan (juta unit)', 'Platform': 'Platform'},
        color_discrete_sequence=px.colors.qualitative.Prism
    )
    fig_platform.update_layout(
        template="plotly_dark",
        yaxis=dict(rangemode="tozero")
    )
    st.plotly_chart(fig_platform, use_container_width=True)

with col2:
    st.subheader("Global Sales Every 5 Year")
    
    # Line chart tren penjualan global per tahun
    yearly_sales = df.groupby('Year')['Global_Sales'].sum().reset_index()
    yearly_sales = yearly_sales[yearly_sales['Year'] <= 2020]
    
    fig_year = px.line(
        yearly_sales,
        x='Year',
        y='Global_Sales',
        markers=True,
        title='Global Sales Trend Over Time',
        labels={'Global_Sales': 'Global Sales (juta unit)', 'Year': 'Year'}
    )
    fig_year.update_layout(
        template="plotly_dark",
        yaxis=dict(rangemode="tozero")
    )
    st.plotly_chart(fig_year, use_container_width=True)

st.write("---")

# Tampilan Tabel Dataset
st.subheader("Dataset Preview")
st.dataframe(df.head(100), use_container_width=True, hide_index=True)