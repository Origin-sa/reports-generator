import os
import sys

def check_required_files():
    """Check if required files exist"""
    files = [
        '../weekly_sales/delivery_app_weekly_sales_2025-04-07_2025-04-13.csv',
        '../weekly_sales/delivery_app_weekly_sales_2025-03-30_2025-04-05.csv'
    ]
    
    missing_files = []
    for file_path in files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    if missing_files:
        print("\nError: Required files are missing:")
        for file in missing_files:
            print(f"- {file}")
        print("\nPlease ensure you have placed the files in the correct location:")
        print("- weekly_sales/")
        print("  - delivery_app_weekly_sales_2025-04-07_2025-04-13.csv")
        print("  - delivery_app_weekly_sales_2025-03-30_2025-04-05.csv")
        sys.exit(1)

def generate_weekly_report():
    """Generate weekly sales report"""
    # File paths
    current_week_file = '../weekly_sales/delivery_app_weekly_sales_2025-04-07_2025-04-13.csv'
    previous_week_file = '../weekly_sales/delivery_app_weekly_sales_2025-03-30_2025-04-05.csv'
    
    # ... rest of the function stays the same ... 