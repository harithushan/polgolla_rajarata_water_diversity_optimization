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
    plot_inflow_vs_release ,
    plot_inflow_vs_release_dam,
    plot_filtered_inflow_vs_release
)

st.set_page_config(page_title="Optimization of water diversity to Rajarata from Polgolla", page_icon="🌊", layout="wide")
st.title("📊 Water Release Analysis: Addressing Water Distribution Challenges in the Rajarata District of Sri Lanka 🌊")

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

add_background_image('static/polgolla-dam-kandy-sri-lanka.jpg')

@st.cache_data
def load_data():
    data = pd.read_csv('data/hydrodata_polgolla_processed_2000-2025_monthly_data.csv')
    data['DATE'] = data['DATE'].str.strip()
    return data

df = load_data()

df['DATE'] = pd.to_datetime(df['DATE'], format='%m/%d/%Y')
df['YEAR'] = df['YEAR'].astype(int)
df['MONTH'] = df['MONTH'].astype(int)

def get_season(month):
    if month in [3, 4]:
        return 'First Inter-Monsoon'
    elif month in [5, 6, 7, 8, 9]:
        return 'Yala'
    elif month in [10, 11]:
        return 'Second Inter-Monsoon'
    else:
        return 'Maha'
df['SEASON'] = df['MONTH'].apply(get_season)

st.markdown(
    """
    <style>
    .stTabs [data-baseweb="tab-list"] {
        background-color: rgba(0, 0, 0, 0.7); 
        border-radius: 12px; 
        padding: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        color: #ffffff;
        font-size: 18px;
        font-weight: bold;
        margin-right: 10px;
    }
    .stTabs [data-baseweb="tab"]:hover {
        background-color: rgba(255, 255, 255, 0.2);
        border-radius: 8px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
    "Home",
    "Analysis over Time",
    "Correlation Matrix",
    "Rajarata vs Victoriya Releases",
    "Monthly Average Releases",
    "Yearly Comparison",
    "Seasonal Water Releases",
    "Inflow vs Release Analysis"
])


with tab1:
    st.markdown("<h1 style='text-align: center; color: #1f4e79;'>Polgolla Dam Water Distribution Analysis</h1>", unsafe_allow_html=True)

    col1, col2 = st.columns([3, 1])

    with col1:
        st.markdown("""
        <div style="background-color: #ffffff; padding: 20px; border-radius: 8px; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);">
        <h3>Introduction to Polgolla Dam</h3>
        The Polgolla Dam is a vital water management structure in Sri Lanka.</br>
        From Polgolla Dam, water is distributed for two main purposes;</br>
        
        - Distribution to the Rajarata area (Diverted through the Ukuwela Powerhouse )
        - Release to the Victoria Dam
        
        <h3>Problem Statement</h3>
        Rajarata area in Sri Lanka experiences relatively low annual rainfall.

        The release of water to Rajarata is inconsistent, despite high inflows in some months.

        Insufficient water availability affects on

        - Agriculture
        - Human consumption
        - Livestock
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.image("static/Picture1.jpg", caption="Polgolla Dam Structure", use_column_width=True)

    st.markdown("### Schematic diagram of Mahaweli multipurpose water resources")
    st.image("static/cascade_Dam.jpg", caption="Schematic diagram of Mahaweli multipurpose water resources", use_column_width=True)
    st.markdown("### Regional Water Distribution Network")
    st.image("static/Picture2.jpg", caption="Water Distribution tunnel", use_column_width=True)

with tab2:
    plot_time_series(df)

with tab3:
    display_correlation_matrix(df)
    
with tab4:
    plot_rajarata_vs_victoriya(df)


with tab5:
    
    plot_monthly_avg_releases(df)
    
    # Year range
    min_year = int(df['DATE'].dt.year.min())
    max_year = int(df['DATE'].dt.year.max())

    start_year = st.selectbox("Start Year", list(range(min_year, max_year + 1)), index=list(range(min_year, max_year + 1)).index(2000))
    end_year = st.selectbox("End Year", list(range(min_year, max_year + 1)), index=list(range(min_year, max_year + 1)).index(2025))

    plot_inflow_vs_release_dam(df, (start_year, end_year), 'RAJARATA_POWER_RELEASE(MCM)', 'Monthly Inflow vs Rajarata Release')
    plot_inflow_vs_release_dam(df, (start_year, end_year), 'VICTORIYA_SPILLWAY_RELEASE(MCM)', 'Monthly Inflow vs Victoria Release')                               
    plot_filtered_inflow_vs_release(df, (start_year, end_year), 'RAJARATA_POWER_RELEASE(MCM)', 'Monthly Inflow vs Rajarata Release')
    plot_filtered_inflow_vs_release(df, (start_year, end_year), 'VICTORIYA_SPILLWAY_RELEASE(MCM)', 'Monthly Inflow vs Victoria Release')                               
    # plot_monthly_inflow_vs_rajarata(df)
    # plot_monthly_inflow_vs_victoriya(df)

with tab6:
    plot_yearly_comparison(df)

with tab7:
    plot_seasonal_releases(df)

with tab8:
    plot_inflow_vs_release(df)
