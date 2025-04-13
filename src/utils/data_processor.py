import pandas as pd

def process_delivery_data(file_path):
    """Process delivery sales data from Foodics export"""
    df = pd.read_excel(file_path)
    # Add data processing logic here
    return df

def process_subscription_data(file_path):
    """Process subscription data from Origin dashboard export"""
    df = pd.read_excel(file_path)
    # Add data processing logic here
    return df

def format_currency(amount):
    """Format amount with currency symbol"""
    return f"SAR {amount:,.2f}" 