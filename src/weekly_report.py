from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from datetime import datetime, timedelta
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import os
import sys
from sales_report import format_currency, SARSymbol

# Define styles
styles = getSampleStyleSheet()
title_style = styles['Title']
number_style = ParagraphStyle(
    'Number',
    fontName='Helvetica',
    fontSize=10,
    alignment=1,  # Right alignment
    spaceAfter=6
)

def check_required_files():
    """Check if required files exist"""
    files = [
        '../weekly_sales/delivery_app_weekly_sales_2025-04-07_2025-04-13.csv',
        '../weekly_sales/delivery_app_weekly_sales_2025-03-31_2025-04-06.csv'
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
        print("  - delivery_app_weekly_sales_2025-03-31_2025-04-06.csv")
        sys.exit(1)

def get_weekly_delivery_data(current_week_file, previous_week_file):
    """Read and process weekly delivery sales data"""
    try:
        # Read current week data
        current_df = pd.read_csv(current_week_file)
        current_metrics = {
            'total_sales': current_df['القيمة'].sum(),  # Sum of 'Value' column
            'total_orders': current_df['العدد'].sum(),  # Sum of 'Count' column
            'net_amount': current_df['المبلغ الصافي'].sum()  # Sum of 'Net Amount' column
        }
        
        # Read previous week data
        previous_df = pd.read_csv(previous_week_file)
        previous_metrics = {
            'total_sales': previous_df['القيمة'].sum(),
            'total_orders': previous_df['العدد'].sum(),
            'net_amount': previous_df['المبلغ الصافي'].sum()
        }
        
        # Calculate week-over-week changes
        sales_change = ((current_metrics['total_sales'] - previous_metrics['total_sales']) / previous_metrics['total_sales']) * 100
        orders_change = ((current_metrics['total_orders'] - previous_metrics['total_orders']) / previous_metrics['total_orders']) * 100
        
        # Add changes to metrics
        current_metrics['sales_change'] = sales_change
        current_metrics['orders_change'] = orders_change
        current_metrics['previous_total_sales'] = previous_metrics['total_sales']
        current_metrics['previous_total_orders'] = previous_metrics['total_orders']
        
        # Add platform breakdown
        current_metrics['platform_breakdown'] = current_df[['طريقة الدفع', 'القيمة', 'العدد', 'المبلغ الصافي']]
        
        return current_metrics
        
    except Exception as e:
        print(f"\nError processing delivery sales data: {str(e)}")
        sys.exit(1)

def get_weekly_subscription_data():
    """Read and process weekly subscription data"""
    try:
        # For now, return empty data since we're focusing on delivery sales comparison
        return {
            'total_new_subs': 0,
            'total_revenue': 0,
            'avg_daily_subs': 0,
            'avg_subscription_value': 0,
            'plan_distribution': {}
        }
    except Exception as e:
        print(f"\nError processing subscription data: {str(e)}")
        sys.exit(1)

def create_weekly_summary_table(delivery_data):
    """Create weekly summary table"""
    # Define styles
    header_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#D84B27')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ])
    
    # Create table data
    data = [
        ['Metric', 'Current Week', 'Previous Week', 'Change'],
        ['Total Sales', 
         Table([[SARSymbol(), Paragraph(f"{delivery_data['total_sales']:,.2f}", number_style)]], 
               style=TableStyle([('ALIGN', (0, 0), (-1, -1), 'CENTER')])),
         Table([[SARSymbol(), Paragraph(f"{delivery_data['previous_total_sales']:,.2f}", number_style)]], 
               style=TableStyle([('ALIGN', (0, 0), (-1, -1), 'CENTER')])),
         Paragraph(f"{delivery_data['sales_change']:+.1f}%", 
                  ParagraphStyle('Change', 
                               textColor=colors.green if delivery_data['sales_change'] >= 0 else colors.red,
                               alignment=1))],
        ['Total Orders', 
         Paragraph(f"{delivery_data['total_orders']:,}", number_style),
         Paragraph(f"{delivery_data['previous_total_orders']:,}", number_style),
         Paragraph(f"{delivery_data['orders_change']:+.1f}%", 
                  ParagraphStyle('Change', 
                               textColor=colors.green if delivery_data['orders_change'] >= 0 else colors.red,
                               alignment=1))]
    ]
    
    # Create table
    table = Table(data, colWidths=[2.5*inch, 2*inch, 2*inch, 1.5*inch])
    table.setStyle(header_style)
    
    # Add cell styles
    table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('TOPPADDING', (0, 1), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    return table

def create_platform_breakdown_table(delivery_data):
    """Create platform breakdown table"""
    # Define styles
    header_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#D84B27')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ])
    
    # Create table data
    data = [['Platform', 'Sales', 'Orders', 'Net Amount']]
    
    for platform in delivery_data['platform_breakdown'].iterrows():
        data.append([
            platform[0],
            Table([[SARSymbol(), Paragraph(f"{platform[1]['القيمة']:,.2f}", number_style)]], 
                  style=TableStyle([('ALIGN', (0, 0), (-1, -1), 'CENTER')])),
            Paragraph(f"{int(platform[1]['العدد']):,}", number_style),
            Table([[SARSymbol(), Paragraph(f"{platform[1]['المبلغ الصافي']:,.2f}", number_style)]], 
                  style=TableStyle([('ALIGN', (0, 0), (-1, -1), 'CENTER')]))
        ])
    
    # Create table
    table = Table(data, colWidths=[1.5*inch, 2*inch, 1.5*inch, 2*inch])
    table.setStyle(header_style)
    
    # Add cell styles
    table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('TOPPADDING', (0, 1), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    return table

def create_daily_metrics_table(delivery_metrics, subscription_metrics):
    """Create a table showing daily metrics"""
    # Merge delivery and subscription metrics
    merged_data = pd.merge(
        delivery_metrics,
        subscription_metrics[['Created at', 'New Subscriptions', 'Total price']],
        left_on='Date',
        right_on='Created at',
        how='outer'
    ).fillna(0)
    
    # Create table data
    table_data = [['Date', 'Sales', 'Orders', 'New Subs', 'Sub Revenue']]
    for _, row in merged_data.iterrows():
        table_data.append([
            row['Date'].strftime('%Y-%m-%d'),
            format_currency(row['Total Sales']),
            f"{int(row['Orders']):,}",
            f"{int(row['New Subscriptions']):,}",
            format_currency(row['Total price'])
        ])
    
    table = Table(table_data, colWidths=[1.2*inch, 1.5*inch, 1.2*inch, 1.2*inch, 1.5*inch])
    table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#D84B27')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ]))
    
    return table

def create_logo():
    """Create logo image for the report"""
    try:
        logo_path = "../assets/images/logos/origin-meals-logo.png"
        if os.path.exists(logo_path):
            # Use a more appropriate size that maintains aspect ratio
            img = Image(logo_path, width=1.5*inch, height=0.75*inch, preserveAspectRatio=True)
            img.hAlign = 'CENTER'
            return img
        else:
            print(f"Warning: Logo file not found at {logo_path}")
            return None
    except Exception as e:
        print(f"Warning: Error creating logo: {str(e)}")
        return None

def generate_weekly_report():
    """Generate weekly sales report"""
    # File paths
    current_week_file = '../weekly_sales/delivery_app_weekly_sales_2025-04-07_2025-04-13.csv'
    previous_week_file = '../weekly_sales/delivery_app_weekly_sales_2025-03-31_2025-04-06.csv'
    
    # Check if files exist
    check_required_files()
    
    # Get data
    delivery_data = get_weekly_delivery_data(current_week_file, previous_week_file)
    
    # Create PDF
    doc = SimpleDocTemplate(
        "../reports/origin_meals_weekly_report_2025-04-07_2025-04-13.pdf",
        pagesize=letter,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=72
    )
    
    story = []
    
    # Add logo
    logo = create_logo()
    if logo:
        story.append(logo)
        story.append(Spacer(1, 20))
    
    # Add title
    title = "Weekly Sales Report (Apr 7 - Apr 13, 2025 vs Mar 31 - Apr 6, 2025)"
    story.append(Paragraph(title, title_style))
    story.append(Spacer(1, 20))
    
    # Add weekly summary
    story.append(Paragraph("Weekly Summary", styles['Heading2']))
    story.append(Spacer(1, 12))
    story.append(create_weekly_summary_table(delivery_data))
    story.append(Spacer(1, 20))
    
    # Add platform breakdown
    story.append(Paragraph("Platform Performance", styles['Heading2']))
    story.append(Spacer(1, 12))
    story.append(create_platform_breakdown_table(delivery_data))
    
    # Build PDF
    doc.build(story)
    
    print("\nWeekly report has been generated: ../reports/origin_meals_weekly_report_2025-04-07_2025-04-13.pdf")
    
    # Print summary to console
    print("\nSales Comparison Summary:")
    print(f"Current Week (Apr 7-13):  {format_currency(delivery_data['total_sales'])}")
    print(f"Previous Week (Mar 31-Apr 6): {format_currency(delivery_data['previous_total_sales'])}")
    print(f"Change: {delivery_data['sales_change']:+.1f}%")

if __name__ == "__main__":
    # Check required files first
    check_required_files()
    generate_weekly_report() 