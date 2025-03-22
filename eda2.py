import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Set page configuration
st.set_page_config(
    page_title="Business Insights Dashboard",
    page_icon="📊",
    layout="wide"
)

# Custom CSS to improve the dashboard appearance
# st.markdown("""
#     <style>
#     .main {
#         padding: 1rem 1rem;
#     }
#     .stTabs [data-baseweb="tab-list"] {
#         gap: 24px;
#     }
#     .stTabs [data-baseweb="tab"] {
#         height: 50px;
#         white-space: pre-wrap;
#         background-color: #f0f2f6;
#         border-radius: 4px 4px 0px 0px;
#         gap: 1px;
#         padding-top: 10px;
#         padding-bottom: 10px;
#     }
#     .stTabs [aria-selected="true"] {
#         background-color: #4e8df5;
#         color: white;
#     }
#     </style>
# """, unsafe_allow_html=True)

# API Configuration
API_URL = "http://localhost:5000"

# Load full data
@st.cache_data
def load_data():
    response = requests.get(f"{API_URL}/data")#"http://localhost:5000/data"
    df = pd.DataFrame(response.json())
    # Convert date strings to datetime
    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'])
    return df

# Filtered data functions
def get_data_by_region(region):
    response = requests.get(f"{API_URL}/data/region/{region}")#"http://localhost:5000/data/region/{region}
    return pd.DataFrame(response.json())

def get_sales_by_customer(customer_type):
    response = requests.get(f"{API_URL}/sales/customer/{customer_type}")
    return pd.DataFrame(response.json())

# Add data
def add_data(new_entry):
    response = requests.post(f"{API_URL}/data/add", json=new_entry)
    return response.json()

# Create graphs and charts
def create_sales_trend(data):
    sales_by_date = data.groupby(data['Date'].dt.strftime('%Y-%m')).agg({
        'Sales': 'sum',
        'Profit': 'sum'
    }).reset_index()
    
    fig = px.line(sales_by_date, x='Date', y=['Sales', 'Profit'], 
                 title='Monthly Sales and Profit Trends',
                 labels={'value': 'Amount', 'variable': 'Metric'})
    return fig

def create_category_breakdown(data):
    category_sales = data.groupby('Category').agg({
        'Sales': 'sum',
        'Profit': 'sum'
    }).reset_index()
    
    fig = px.bar(category_sales, x='Category', y='Sales', 
                text='Sales', color='Profit',
                title='Sales by Category',
                labels={'Sales': 'Total Sales', 'Profit': 'Total Profit'})
    fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    return fig

def create_region_map(data):
    region_data = data.groupby('Region').agg({
        'Sales': 'sum',
        'Profit': 'sum'
    }).reset_index()
    
    fig = px.choropleth(region_data, 
                       locations='Region', 
                       color='Sales',
                       title='Sales by Region',
                       labels={'Sales': 'Total Sales'})
    return fig

def create_customer_pie(data):
    customer_data = data.groupby('Customer_Type').agg({
        'Sales': 'sum'
    }).reset_index()
    
    fig = px.pie(customer_data, values='Sales', names='Customer_Type',
                title='Sales Distribution by Customer Type')
    return fig

# Main App
def main():
    st.title("📊 Business Insights Dashboard")
    
    # Load the data
    data = load_data()
    
    # Dashboard tabs
    tabs = st.tabs(["📈 Overview", "🔍 Detailed Analysis", "📝 Data Management", "📊 Custom Reports"])
    
    # Tab 1: Overview
    with tabs[0]:
        st.header("Business Performance Overview")
        
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Sales", f"${data['Sales'].sum():,.2f}")
        with col2:
            st.metric("Total Profit", f"${data['Profit'].sum():,.2f}")
        with col3:
            profit_margin = (data['Profit'].sum() / data['Sales'].sum()) * 100
            st.metric("Profit Margin", f"{profit_margin:.2f}%")
        with col4:
            st.metric("Total Products", f"{data['Product'].nunique()}")
        
        # Charts
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(create_sales_trend(data), use_container_width=False)
        with col2:
            st.plotly_chart(create_category_breakdown(data), use_container_width=False)
        
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(create_region_map(data), use_container_width=True)
        with col2:
            st.plotly_chart(create_customer_pie(data), use_container_width=True)
    
    # Tab 2: Detailed Analysis
    with tabs[1]:
        st.header("Detailed Data Analysis")
        
        # Filter options
        col1, col2, col3 = st.columns(3)
        with col1:
            selected_region = st.selectbox("Select Region", ["All"] + list(data['Region'].unique()))
        with col2:
            selected_category = st.selectbox("Select Category", ["All"] + list(data['Category'].unique()))
        with col3:
            selected_customer = st.selectbox("Select Customer Type", ["All"] + list(data['Customer_Type'].unique()))
        
        # Apply filters
        filtered_data = data.copy()
        if selected_region != "All":
            filtered_data = filtered_data[filtered_data['Region'] == selected_region]
        if selected_category != "All":
            filtered_data = filtered_data[filtered_data['Category'] == selected_category]
        if selected_customer != "All":
            filtered_data = filtered_data[filtered_data['Customer_Type'] == selected_customer]
        
        # Display filtered data
        st.subheader("Filtered Dataset")
        st.dataframe(filtered_data, use_container_width=True)
        
        # Additional analysis
        if not filtered_data.empty:
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Top 5 Products by Sales")
                top_products = filtered_data.groupby('Product').agg({
                    'Sales': 'sum'
                }).sort_values('Sales', ascending=False).head(5).reset_index()
                fig = px.bar(top_products, x='Product', y='Sales', 
                           title='Top 5 Products by Sales',
                           color='Sales')
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.subheader("Discount Analysis")
                discount_data = filtered_data.groupby('Discount').agg({
                    'Sales': 'sum',
                    'Profit': 'sum'
                }).reset_index()
                fig = px.scatter(discount_data, x='Discount', y='Sales', size='Profit',
                               title='Impact of Discount on Sales and Profit',
                               labels={'Discount': 'Discount Rate', 'Sales': 'Total Sales'})
                st.plotly_chart(fig, use_container_width=True)
    
    # Tab 3: Data Management
    with tabs[2]:
        st.header("Data Management")
        
        st.subheader("Add New Data Entry")
        with st.form("new_data_form"):
            col1, col2 = st.columns(2)
            with col1:
                date = st.date_input("Date", datetime.now())
                product = st.text_input("Product")
                category = st.selectbox("Category", ["Electronics", "Furniture", "Clothing", "Kitchen"])
                region = st.selectbox("Region", data['Region'].unique())
            with col2:
                sales = st.number_input("Sales", min_value=0)
                profit = st.number_input("Profit", min_value=0)
                discount = st.number_input("Discount", min_value=0.0, max_value=1.0)
                customer_type = st.selectbox("Customer Type", ["Regular", "New", "VIP"])

            submitted = st.form_submit_button("Add Data")
            if submitted:
                new_entry = {
                    "Date": date.strftime("%Y-%m-%d"),
                    "Product": product,
                    "Category": category,
                    "Sales": sales,
                    "Profit": profit,
                    "Discount": discount,
                    "Region": region,
                    "Customer_Type": customer_type
                }
                response = add_data(new_entry)
                st.success(response.get('message', 'Error adding data'))
                st.experimental_rerun()  # Refresh the dashboard
        
        # View the full dataset
        with st.expander("View Full Dataset"):
            st.dataframe(data, use_container_width=True)
    
    # Tab 4: Custom Reports
    with tabs[3]:
        st.header("Custom Reports")
        
        report_type = st.selectbox("Select Report Type", [
            "Sales by Region", 
            "Performance by Customer Type",
            "Category Analysis",
            "Discount Impact Analysis"
        ])
        
        if report_type == "Sales by Region":
            region = st.selectbox("Select Region for Detailed Report", data['Region'].unique())
            if st.button("Generate Report"):
                region_data = get_data_by_region(region)
                
                st.subheader(f"Detailed Report for {region}")
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Total Sales", f"${region_data['Sales'].sum():,.2f}")
                    st.metric("Total Profit", f"${region_data['Profit'].sum():,.2f}")
                
                with col2:
                    category_data = region_data.groupby('Category').agg({
                        'Sales': 'sum'
                    }).reset_index()
                    fig = px.pie(category_data, values='Sales', names='Category',
                               title=f'Category Distribution in {region}')
                    st.plotly_chart(fig, use_container_width=True)
                
                # Time trend
                sales_trend = region_data.groupby(pd.to_datetime(region_data['Date']).dt.strftime('%Y-%m')).agg({
                    'Sales': 'sum',
                    'Profit': 'sum'
                }).reset_index()
                
                fig = px.line(sales_trend, x='Date', y=['Sales', 'Profit'],
                             title=f'Monthly Performance in {region}')
                st.plotly_chart(fig, use_container_width=True)
                
                st.dataframe(region_data, use_container_width=True)
        
        elif report_type == "Performance by Customer Type":
            customer_type = st.selectbox("Select Customer Type", data['Customer_Type'].unique())
            if st.button("Generate Report"):
                customer_data = get_sales_by_customer(customer_type)
                
                st.subheader(f"Detailed Report for {customer_type} Customers")
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Total Sales", f"${customer_data['Sales'].sum():,.2f}")
                    st.metric("Average Discount", f"{customer_data['Discount'].mean()*100:.2f}%")
                
                with col2:
                    region_distribution = customer_data.groupby('Region').agg({
                        'Sales': 'sum'
                    }).reset_index()
                    fig = px.bar(region_distribution, x='Region', y='Sales',
                               title=f'Regional Distribution of {customer_type} Customers')
                    st.plotly_chart(fig, use_container_width=True)
                
                st.dataframe(customer_data, use_container_width=True)
        
        elif report_type == "Category Analysis":
            category = st.selectbox("Select Product Category", data['Category'].unique())
            if st.button("Generate Report"):
                category_data = data[data['Category'] == category]
                
                st.subheader(f"Detailed Analysis of {category} Category")
                
                # Metrics
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Sales", f"${category_data['Sales'].sum():,.2f}")
                with col2:
                    st.metric("Total Profit", f"${category_data['Profit'].sum():,.2f}")
                with col3:
                    category_margin = (category_data['Profit'].sum() / category_data['Sales'].sum()) * 100
                    st.metric("Profit Margin", f"{category_margin:.2f}%")
                
                # Top products
                top_products = category_data.groupby('Product').agg({
                    'Sales': 'sum',
                    'Profit': 'sum'
                }).sort_values('Sales', ascending=False).head(10).reset_index()
                
                fig = px.bar(top_products, x='Product', y=['Sales', 'Profit'],
                           barmode='group', title=f'Top Products in {category} Category')
                st.plotly_chart(fig, use_container_width=True)
                
                st.dataframe(category_data, use_container_width=True)
        
        elif report_type == "Discount Impact Analysis":
            if st.button("Generate Report"):
                # Group data by discount ranges
                data['DiscountBin'] = pd.cut(data['Discount'], 
                                           bins=[0, 0.1, 0.2, 0.3, 0.4, 0.5, 1.0],
                                           labels=['0-10%', '10-20%', '20-30%', '30-40%', '40-50%', '50-100%'])
                
                discount_analysis = data.groupby('DiscountBin').agg({
                    'Sales': 'sum',
                    'Profit': 'sum',
                    'Product': 'count'
                }).reset_index()
                
                discount_analysis['ProfitMargin'] = (discount_analysis['Profit'] / discount_analysis['Sales']) * 100
                
                st.subheader("Discount Impact Analysis")
                
                col1, col2 = st.columns(2)
                with col1:
                    fig = px.bar(discount_analysis, x='DiscountBin', y='Sales',
                               title='Sales by Discount Range')
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    fig = px.line(discount_analysis, x='DiscountBin', y='ProfitMargin',
                                markers=True, title='Profit Margin by Discount Range')
                    st.plotly_chart(fig, use_container_width=True)
                
                st.subheader("Discount Range Data")
                st.dataframe(discount_analysis, use_container_width=True)

if __name__ == "__main__":
    main()