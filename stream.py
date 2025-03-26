import streamlit as st
import pandas as pd
from PIL import Image
import base64
from utils import(
    plot_time_series,
    plot_rajarata_vs_victoriya,
    plot_monthly_inflow_vs_rajarata,
    plot_monthly_inflow_vs_victoriya,
    plot_monthly_avg_releases,
    plot_yearly_comparison,
    display_correlation_matrix,
    plot_seasonal_releases,
    plot_inflow_vs_release 
)

st.set_page_config(page_title="Optimization of water diversity to Rajarata from Polgolla", page_icon="🌊", layout="wide")
def add_background_image(image_path):
    with open(image_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode()
    image_url = f"data:image/png;base64,{encoded_image}"
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url({image_url});
            background-size: cover;
            background-position: center;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

# Add a background image
add_background_image('static\Polgolla-diversion-dam.png')
# Load your dataset
@st.cache_data
def load_data():
    # Replace 'your_dataset.csv' with the path to your actual data file
    data = pd.read_csv('data/hydrodata_polgolla_processed_2000-2025_monthly_data.csv')
    data['DATE'] = data['DATE'].str.strip()
    return data

df = load_data()

# Data Preprocessing
df['DATE'] = pd.to_datetime(df['DATE'], format='%m/%d/%Y')
df['YEAR'] = df['YEAR'].astype(int)
df['MONTH'] = df['MONTH'].astype(int)

def get_season(month):
    if month in [3, 4]:
        return 'First Inter-Monsoon'
    elif month in [5, 6, 7, 8]:
        return 'Yala'
    elif month in [9]:
        return 'Second Inter-Monsoon'
    else:
        return 'Maha'
df['SEASON'] = df['MONTH'].apply(get_season)

# Add season column
# def get_season(month):
#     if month in [12, 1, 2]:
#         return 'Winter'
#     elif month in [3, 4, 5]:
#         return 'Spring'
#     elif month in [6, 7, 8]:
#         return 'Summer'
#     else:
#         return 'Fall'
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "Time Series Analysis",
    "Rajarata vs Victoriya Releases",
    "Monthly Average Releases",
    "Yearly Comparison",
    "Correlation Matrix",
    "Seasonal Water Releases",
    "Inflow vs Release Analysis"
])
with tab1:
    plot_time_series()

with tab2:
    plot_rajarata_vs_victoriya()

with tab3:
    plot_monthly_avg_releases()
    plot_monthly_inflow_vs_rajarata(df)
    plot_monthly_inflow_vs_victoriya(df)

with tab4:
    plot_yearly_comparison()

with tab5:
    display_correlation_matrix()
with tab6:
    plot_seasonal_releases()

with tab7:
    plot_inflow_vs_release()
