# Reports Generator

A Python-based tool for generating daily sales reports for Origin Meals, including delivery and subscription metrics.

## Features

- Generates comprehensive sales reports in PDF format
- Tracks delivery sales across multiple platforms
- Monitors subscription performance and growth
- Provides detailed revenue analysis
- Includes visual metrics and comparisons

## Requirements

- Python 3.8 or higher
- Required Python packages:
  - pandas
  - reportlab
  - openpyxl

## Installation

1. Clone the repository:

```bash
git clone git@github.com:Origin-sa/reports-generator.git
cd reports-generator
```

2. Install required packages:

```bash
python3 -m pip install -r requirements.txt
```

## Usage

1. Place your data files in the appropriate directories:

   - Delivery sales data in `delivery_sales/`
   - Subscription data in `subscription_sales/`

2. Run the report generator:

```bash
python3 sales_report.py
```

3. The generated report will be saved as `origin_meals_sales_report_YYYY-MM-DD.pdf`

## Report Contents

### Delivery Sales

- Total sales and orders
- Platform breakdown
- Daily comparisons
- Revenue analysis

### Subscription Sales

- Total active subscriptions
- New subscriptions tracking
- Revenue metrics
- Average subscription value

## Data Sources

- Delivery sales data: Exported CSV files from Foodics platform
- Subscription data: Exported data from Origin subscription dashboard
