# Reports Generator

A Python-based tool for generating daily sales reports for Origin Meals, including delivery and subscription metrics.

## Features

- Generates comprehensive sales reports in PDF format
- Tracks delivery sales across multiple platforms
- Monitors subscription performance and growth
- Provides detailed revenue analysis
- Includes visual metrics and comparisons

## Project Structure

```
reports-generator/
├── src/
│   ├── data/
│   │   ├── delivery_sales/     # Foodics export files
│   │   └── subscription_sales/ # Origin dashboard export files
│   ├── utils/                  # Utility functions
│   │   ├── data_processor.py   # Data processing utilities
│   │   └── pdf_generator.py    # PDF generation utilities
│   └── sales_report.py         # Main report generation script
├── assets/
│   ├── images/
│   │   └── logos/             # Company logos
│   ├── icons/
│   │   └── currency/          # Currency symbols
│   └── fonts/                 # Custom fonts
├── reports/                   # Generated PDF reports
├── requirements.txt           # Python dependencies
└── README.md                 # Project documentation

```

## Requirements

- Python 3.8 or higher
- Required Python packages:
  - pandas
  - reportlab
  - openpyxl
  - svglib
  - matplotlib

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

   - Delivery sales data: Place Foodics CSV exports in `src/data/delivery_sales/`
   - Subscription data: Place Origin dashboard exports in `src/data/subscription_sales/`

2. Run the report generator:

```bash
python3 src/sales_report.py
```

3. The generated report will be saved in the `reports` directory as:
   ```
   reports/origin_meals_sales_report_YYYY-MM-DD.pdf
   ```

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

## Assets

- Company logos and images are stored in `assets/images/`
- Currency symbols and icons in `assets/icons/`
- Custom fonts in `assets/fonts/`

## Notes

- Reports are generated with the current date in the filename
- All monetary values are in Saudi Riyal (﷼)
- Percentage changes are color-coded (green for positive, red for negative)
