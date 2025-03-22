from flask import Flask, request, jsonify
import pandas as pd
from flasgger import Swagger

app = Flask(__name__)
swagger = Swagger(app)

# Load dataset
data = pd.read_csv('data/data.csv')

# ----------- GET METHODS -----------

@app.route('/', methods=['GET'])
def welcome():
    """
    Welcome Message
    ---
    responses:
      200:
        description: Welcome message for the EDA Dashboard API
    """
    return jsonify({
        "message": "Welcome to the EDA Dashboard API! 🚀",
        "endpoints": {
            "/data": "Get full dataset",
            "/data/region/<region>": "Get data filtered by region",
            "/sales/customer/<customer_type>": "Get total sales by customer type",
            "/data/add": "Add new data entry (POST method)"
        }
    })

# 1. Get full dataset
@app.route('/data', methods=['GET'])
def get_data():
    """
    Get Full Dataset
    ---
    responses:
      200:
        description: Returns the full dataset
    """
    return jsonify(data.to_dict(orient='records'))


# 2. Get data filtered by region
@app.route('/data/region/<region>', methods=['GET'])
def get_data_by_region(region):
    """
    Get Data Filtered by Region
    ---
    parameters:
      - name: region
        in: path
        type: string
        required: true
        description: The region to filter by
    responses:
      200:
        description: Data filtered by the specified region
      404:
        description: Region not found
    """
    filtered_data = data[data['Region'].str.lower() == region.lower()]
    if filtered_data.empty:
        return jsonify({"error": "Region not found"}), 404
    return jsonify(filtered_data.to_dict(orient='records'))

# 3. Get sales by customer type
@app.route('/sales/customer/<customer_type>', methods=['GET'])
def get_sales_by_customer(customer_type):
    """
    Get Sales by Customer Type
    ---
    parameters:
      - name: customer_type
        in: path
        type: string
        required: true
        description: The customer type to filter by
    responses:
      200:
        description: Total sales by customer type
      404:
        description: Customer type not found
    """
    filtered_data = data[data['Customer_Type'].str.lower() == customer_type.lower()]
    if filtered_data.empty:
        return jsonify({"error": "Customer type not found"}), 404
    total_sales = filtered_data['Sales'].sum()
    return jsonify({"Customer_Type": customer_type, "Total_Sales": total_sales})

# ----------- POST METHOD -----------

@app.route('/data/add', methods=['POST'])
def add_data():
    """
    Add New Data Entry
    ---
    parameters:
      - name: new_entry
        in: body
        required: true
        schema:
          id: NewEntry
          required:
            - Date
            - Product
            - Category
            - Sales
            - Profit
            - Discount
            - Region
            - Customer_Type
          properties:
            Date:
              type: string
            Product:
              type: string
            Category:
              type: string
            Sales:
              type: number
            Profit:
              type: number
            Discount:
              type: number
            Region:
              type: string
            Customer_Type:
              type: string
    responses:
      201:
        description: Data added successfully
      400:
        description: Missing required fields
      500:
        description: Server error
    """
    try:
        new_entry = request.get_json()

        # Data validation
        required_fields = ['Date', 'Product', 'Category', 'Sales', 'Profit', 'Discount', 'Region', 'Customer_Type']
        if not all(field in new_entry for field in required_fields):
            return jsonify({"error": "Missing required fields"}), 400

        # Append new entry
        global data
        data = pd.concat([data, pd.DataFrame([new_entry])], ignore_index=True)
        return jsonify({"message": "Data added successfully"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ----------- RUN THE APP -----------
if __name__ == '__main__':
    app.run(debug=True)
