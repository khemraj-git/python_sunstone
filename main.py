import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

try:
    # Read CSV without parse_dates errors
    try:
        sales_data = pd.read_csv('sales_data_sample.csv', encoding='latin-1')
    except UnicodeDecodeError:
        try:
            sales_data = pd.read_csv('sales_data_sample.csv', encoding='windows-1252')
        except UnicodeDecodeError:
            sales_data = pd.read_csv('sales_data_sample.csv', encoding='cp1252')

except FileNotFoundError:
    print("Error: 'sales_data_sample.csv' not found. Please ensure the file is in the same directory as the script or provide the correct path.")
    exit()

# Parse dates separately with error handling
try:
    sales_data['ORDERDATE'] = pd.to_datetime(sales_data['ORDERDATE'], errors='coerce')
except KeyError:
    print("Error: ORDERDATE column not found.")
    exit()
# Drop rows with invalid dates after attempting to parse.
sales_data.dropna(subset=['ORDERDATE'], inplace=True)

# Basic data cleaning (example: handling missing values)
sales_data.dropna(inplace=True)  # Remove rows with missing values

# --- Task 2: Perform Summary Statistics and Exploratory Analysis ---

# Display basic statistics
print("Summary Statistics:")
print(sales_data.describe())

# Display data types and check for any inconsistencies
print("\nData Types:")
print(sales_data.dtypes)

# Example: Check for unique values in a categorical column (e.g., product category)
if 'PRODUCTLINE' in sales_data.columns:
    print("\nUnique Product Categories:")
    print(sales_data['PRODUCTLINE'].unique())

# --- Task 3: Visualize Key Metrics ---

# Example: Sales trend over time (assuming there's a 'ORDERDATE' column)
if 'ORDERDATE' in sales_data.columns:
    sales_data.set_index('ORDERDATE', inplace=True)
    monthly_sales = sales_data['SALES'].resample('MS').sum() #sum sales by month.
    plt.figure(figsize=(12, 6))
    monthly_sales.plot()
    plt.title('Monthly Sales Trend')
    plt.xlabel('Month')
    plt.ylabel('Sales')
    plt.grid(True)
    plt.show()

# Example: Top-performing products (assuming there's a 'PRODUCTLINE' and 'SALES' column)
if 'PRODUCTLINE' in sales_data.columns and 'SALES' in sales_data.columns:
    product_sales = sales_data.groupby('PRODUCTLINE')['SALES'].sum().sort_values(ascending=False).head(10)
    plt.figure(figsize=(10, 6))
    product_sales.plot(kind='bar')
    plt.title('Top 10 Performing Products')
    plt.xlabel('Product')
    plt.ylabel('Total Sales')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

# Example: Seasonal patterns (if applicable)
#If you have a date column, you can extract month or day of week to find seasonal patterns.
if 'ORDERDATE' in sales_data.index:
    sales_data['Month'] = sales_data.index.month
    monthly_avg_sales = sales_data.groupby('Month')['SALES'].mean()
    plt.figure(figsize=(10, 6))
    monthly_avg_sales.plot(kind='line', marker='o')
    plt.title('Average Monthly Sales')
    plt.xlabel('Month')
    plt.ylabel('Average Sales')
    plt.xticks(range(1, 13))
    plt.grid(True)
    plt.show()

