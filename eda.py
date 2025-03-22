import streamlit as st
import requests
import pandas as pd
import json

API_URL = "http://localhost:5000"

# Load full data
@st.cache_data
def load_data():
    try:
        response = requests.get(f"{API_URL}/data")
        return pd.DataFrame(response.json())
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

# Filtered data functions
def get_data_by_region(region):
    try:
        response = requests.get(f"{API_URL}/data/region/{region}")
        return pd.DataFrame(response.json())
    except Exception as e:
        st.error(f"Error getting region data: {e}")
        return pd.DataFrame()

def get_sales_by_customer(customer_type):
    try:
        response = requests.get(f"{API_URL}/sales/customer/{customer_type}")
        return pd.DataFrame(response.json())
    except Exception as e:
        st.error(f"Error getting customer sales data: {e}")
        return pd.DataFrame()

# Add data
def add_data(new_entry):
    try:
        response = requests.post(f"{API_URL}/data/add", json=new_entry)
        return response.json()
    except Exception as e:
        st.error(f"Error adding data: {e}")
        return {"message": f"Error: {str(e)}"}

# Page configuration
st.set_page_config(
    page_title="EDA Dashboard",
    page_icon="📊",
    layout="wide"
)

# Streamlit UI
st.title("📊 EDA Dashboard with Flask API Integration")

# Create tabs for different sections
tab1, tab2, tab3, tab4 = st.tabs(["Full Dataset", "Filter by Region", "Sales by Customer", "Add New Data"])

# Load the data once
data = load_data()

# Tab 1: Full Dataset
with tab1:
    st.subheader("Full Dataset")
    st.dataframe(data, use_container_width=True)
    
    # Add some basic statistics
    if not data.empty:
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Sales", f"${data['Sales'].sum():,.2f}")
        with col2:
            st.metric("Total Profit", f"${data['Profit'].sum():,.2f}")
        
        # Add a simple chart
        st.subheader("Sales by Category")
        category_sales = data.groupby('Category')['Sales'].sum().reset_index()
        st.bar_chart(category_sales.set_index('Category'))

# Tab 2: Filter by Region
with tab2:
    st.subheader("Filter Data by Region")
    
    # Only show the selectbox if data is available
    if not data.empty and 'Region' in data.columns:
        region = st.selectbox("Select Region", data['Region'].unique(), key="region_filter")
        if st.button("Filter by Region"):
            filtered_data = get_data_by_region(region)
            
            if not filtered_data.empty:
                st.dataframe(filtered_data, use_container_width=True)
                
                # Show region-specific metrics
                st.subheader(f"Summary for {region}")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Region Sales", f"${filtered_data['Sales'].sum():,.2f}")
                with col2:
                    st.metric("Region Profit", f"${filtered_data['Profit'].sum():,.2f}")
                with col3:
                    if 'Discount' in filtered_data.columns:
                        st.metric("Avg. Discount", f"{filtered_data['Discount'].mean():.1%}")
            else:
                st.info(f"No data available for region: {region}")
    else:
        st.warning("No region data available.")

# Tab 3: Sales by Customer Type
with tab3:
    st.subheader("Sales by Customer Type")
    
    # Only show the selectbox if data is available
    if not data.empty and 'Customer_Type' in data.columns:
        customer_type = st.selectbox("Select Customer Type", data['Customer_Type'].unique(), key="customer_filter")
        if st.button("Get Sales Data"):
            sales_data = get_sales_by_customer(customer_type)
            
            if not sales_data.empty:
                st.dataframe(sales_data, use_container_width=True)
                
                # Show customer-specific metrics
                st.subheader(f"Summary for {customer_type} Customers")
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Total Sales", f"${sales_data['Sales'].sum():,.2f}")
                with col2:
                    st.metric("Total Profit", f"${sales_data['Profit'].sum():,.2f}")
                
                # Add a chart for customer sales by category if available
                if 'Category' in sales_data.columns:
                    st.subheader(f"{customer_type} Sales by Category")
                    customer_cat_sales = sales_data.groupby('Category')['Sales'].sum().reset_index()
                    st.bar_chart(customer_cat_sales.set_index('Category'))
            else:
                st.info(f"No data available for customer type: {customer_type}")
    else:
        st.warning("No customer data available.")

# Tab 4: Add New Data Entry
with tab4:
    st.subheader("Add New Data Entry")
    
    with st.form("new_data_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            date = st.date_input("Date")
            product = st.text_input("Product")
            category = st.selectbox("Category", ["Electronics", "Furniture", "Clothing", "Kitchen"])
            sales = st.number_input("Sales", min_value=0)
        
        with col2:
            profit = st.number_input("Profit", min_value=0)
            discount = st.number_input("Discount", min_value=0.0, max_value=1.0, format="%.2f")
            
            # Use existing data for dropdowns if available
            if not data.empty and 'Region' in data.columns:
                region = st.selectbox("Region", data['Region'].unique())
            else:
                region = st.text_input("Region")
                
            customer_type = st.selectbox("Customer Type", ["Regular", "New", "VIP"])
        
        submitted = st.form_submit_button("Add Data")
        
        if submitted:
            # Validate inputs
            if not product:
                st.error("Product name is required.")
            elif sales <= 0:
                st.error("Sales must be greater than zero.")
            else:
                new_entry = {
                    "Date": date.strftime("%Y-%m-%d"),
                    "Product": product,
                    "Category": category,
                    "Sales": float(sales),
                    "Profit": float(profit),
                    "Discount": float(discount),
                    "Region": region,
                    "Customer_Type": customer_type
                }
                
                # Show what's being sent
                with st.expander("Data being submitted"):
                    st.json(new_entry)
                
                response = add_data(new_entry)
                
                if 'message' in response and 'Error' not in response['message']:
                    st.success(response['message'])
                    st.info("Refreshing data in 3 seconds...")
                    st.experimental_rerun()
                else:
                    st.error(response.get('message', 'Unknown error occurred'))

# Add footer
st.markdown("---")
st.caption("EDA Dashboard with Flask API Integration")