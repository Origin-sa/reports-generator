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
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF
from reportlab.platypus import Flowable
import os

class SARSymbol(Flowable):
    def __init__(self, width=10, height=10):
        Flowable.__init__(self)
        self.width = width
        self.height = height
        
    def draw(self):
        svg_path = 'assets/icons/currency/sar-symbol.svg'
        if os.path.exists(svg_path):
            drawing = svg2rlg(svg_path)
            # Scale to match text height
            scale = self.height / drawing.height
            drawing.scale(scale, scale)
            drawing.drawOn(self.canv, 0, 0)

def create_logo():
    # Use the actual logo image
    logo_path = 'assets/images/logos/origin-meals-logo.png'
    if os.path.exists(logo_path):
        # Create image with fixed dimensions
        logo = Image(logo_path)
        # Set a fixed width and maintain aspect ratio
        logo.drawWidth = 2 * inch
        logo.drawHeight = 1.5 * inch  # Approximate height, adjust as needed
        logo.hAlign = 'CENTER'  # Center align the logo
        return logo
    else:
        print(f"Warning: Logo file {logo_path} not found")
        return None

def format_currency(amount):
    """Format amount with SAR symbol from SVG"""
    from reportlab.platypus import Table, TableStyle
    
    # Create a small table to hold the symbol and amount side by side
    symbol = SARSymbol(width=4, height=8)  # Further reduced size
    amount_text = Paragraph(f"{amount:,.2f}", ParagraphStyle('Amount', alignment=1))
    
    # Create a mini-table for the currency
    currency_table = Table(
        [[symbol, amount_text]], 
        colWidths=[3, None],  # Further reduced symbol width
        rowHeights=[8]  # Further reduced row height
    )
    
    # Style the mini-table
    currency_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (0, 0), 0),     # No left padding for symbol
        ('RIGHTPADDING', (0, 0), (0, 0), 0),    # No right padding for symbol
        ('LEFTPADDING', (1, 0), (1, 0), -2),    # Negative padding to move number closer
        ('RIGHTPADDING', (1, 0), (1, 0), 0),    # No right padding for amount
        ('TOPPADDING', (0, 0), (-1, -1), 0),    # No top padding
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0), # No bottom padding
    ]))
    
    return currency_table

def get_delivery_data():
    """Read and process delivery sales data from CSV files"""
    # Read CSV files
    today_df = pd.read_csv('sales/delivery_app_today_sales.csv')
    yesterday_df = pd.read_csv('sales/delivery_app_yesterday_sales.csv')
    
    # Calculate totals
    today_sales = today_df['المبلغ الصافي'].sum()
    today_orders = today_df['العدد'].sum()
    today_platforms = len(today_df)
    
    yesterday_sales = yesterday_df['المبلغ الصافي'].sum()
    yesterday_orders = yesterday_df['العدد'].sum()
    yesterday_platforms = len(yesterday_df)
    
    # Calculate changes
    sales_change = ((today_sales - yesterday_sales) / yesterday_sales) * 100 if yesterday_sales != 0 else 0
    orders_change = ((today_orders - yesterday_orders) / yesterday_orders) * 100 if yesterday_orders != 0 else 0
    platforms_change = ((today_platforms - yesterday_platforms) / yesterday_platforms) * 100 if yesterday_platforms != 0 else 0
    
    return {
        'metrics': {
            'today_sales': today_sales,
            'today_orders': today_orders,
            'today_platforms': today_platforms,
            'yesterday_sales': yesterday_sales,
            'yesterday_orders': yesterday_orders,
            'yesterday_platforms': yesterday_platforms,
            'sales_change': sales_change,
            'orders_change': orders_change,
            'platforms_change': platforms_change
        },
        'platform_breakdown': today_df
    }

def get_subscription_data():
    """Read and process subscription data from Excel file"""
    # Read Excel file
    df = pd.read_excel('subscription_sales/DatatableExport (2).xlsx')
    
    # Process subscription data
    total_subscriptions = len(df)
    total_revenue = df['Total price'].sum() if 'Total price' in df.columns else 0
    
    # Set the report date to April 13, 2025
    report_date = pd.Timestamp('2025-04-13')
    yesterday = report_date - pd.Timedelta(days=1)
    
    # Count new users for today and yesterday
    new_users_today = 0
    new_users_yesterday = 0
    new_users_revenue = 0
    
    if 'Created at' in df.columns:
        # Convert dates with day first format (DD/MM/YYYY)
        df['Created at'] = pd.to_datetime(df['Created at'], format='%d/%m/%Y', errors='coerce')
        new_users_today = len(df[df['Created at'].dt.normalize() == report_date])
        new_users_yesterday = len(df[df['Created at'].dt.normalize() == yesterday])
        # Calculate revenue from new users today
        new_users_revenue = df[df['Created at'].dt.normalize() == report_date]['Total price'].sum() if 'Total price' in df.columns else 0
    
    # Calculate change percentage
    new_users_change = ((new_users_today - new_users_yesterday) / new_users_yesterday * 100) if new_users_yesterday != 0 else 0
    
    # Extract additional metrics
    subscription_metrics = {
        'plan_distribution': df['Plan'].value_counts().to_dict() if 'Plan' in df.columns else {},
        'payment_methods': df['Payment method'].value_counts().to_dict() if 'Payment method' in df.columns else {},
        'status_distribution': df['Status'].value_counts().to_dict() if 'Status' in df.columns else {},
        'avg_subscription_value': total_revenue / total_subscriptions if total_subscriptions > 0 else 0,
        'new_users_revenue': new_users_revenue
    }
    
    return {
        'total_subscriptions': total_subscriptions,
        'total_revenue': total_revenue,
        'new_users_today': new_users_today,
        'new_users_yesterday': new_users_yesterday,
        'new_users_change': new_users_change,
        'metrics': subscription_metrics,
        'details': df
    }

def create_table_style(has_header=True):
    """Create common table style"""
    style = [
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]
    
    if has_header:
        style.extend([
            ('BACKGROUND', (0, 0), (-1, 0), HexColor('#D84B27')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('TOPPADDING', (0, 0), (-1, 0), 8),
        ])
    
    return TableStyle(style)

def generate_sales_report():
    # Get sales data
    delivery_data = get_delivery_data()
    subscription_data = get_subscription_data()
    
    # Create a PDF document with date in filename
    report_date = "2025-04-12"
    report_path = os.path.join('reports', f"origin_meals_sales_report_{report_date}.pdf")
    doc = SimpleDocTemplate(
        report_path,
        pagesize=letter,
        rightMargin=36,  # Reduced margins
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    # Define paths to assets
    svg_path = 'assets/icons/currency/sar-symbol.svg'
    logo_path = 'assets/images/logos/origin-meals-logo.png'

    # Create styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=20,
        spaceAfter=15,
        alignment=1
    )
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Heading2'],
        fontName='Helvetica',
        fontSize=9,
        spaceAfter=10,
        alignment=0
    )
    section_style = ParagraphStyle(
        'Section',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=12,
        spaceAfter=5,
        alignment=0
    )
    platform_style = ParagraphStyle(
        'Platform',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=12,
        spaceAfter=5
    )
    number_style = ParagraphStyle(
        'Number',
        fontName='Helvetica',
        fontSize=10,
        leading=12,
        alignment=1
    )

    # Create story list to hold elements
    story = []

    # Add logo
    logo = create_logo()
    if logo:
        logo.drawWidth = 1.5 * inch  # Reduced logo size
        logo.drawHeight = 1 * inch
        story.append(logo)
        story.append(Spacer(1, 10))

    # Add title with fixed date
    story.append(Paragraph(f"Sales Report - {report_date}", title_style))
    story.append(Spacer(1, 10))

    # Add Delivery Sales Section
    story.append(Paragraph("Delivery Sales", section_style))
    story.append(Spacer(1, 10))
    
    # Create delivery metrics table
    metrics = delivery_data['metrics']
    
    def format_change(value):
        if value >= 0:
            return f"<font color='green'>+{value:.1f}%</font>"
        else:
            return f"<font color='red'>{value:+.1f}%</font>"
    
    delivery_table_data = [
        ['Metric', 'Today', 'Yesterday', 'Change'],
        [
            Paragraph('Total Sales', number_style),
            format_currency(metrics['today_sales']),
            format_currency(metrics['yesterday_sales']),
            Paragraph(format_change(metrics['sales_change']), number_style)
        ],
        [
            Paragraph('Total Orders', number_style),
            Paragraph(f"{int(metrics['today_orders']):,}", number_style),
            Paragraph(f"{int(metrics['yesterday_orders']):,}", number_style),
            Paragraph(format_change(metrics['orders_change']), number_style)
        ],
        [
            Paragraph('Active Platforms', number_style),
            Paragraph(f"{metrics['today_platforms']}", number_style),
            Paragraph(f"{metrics['yesterday_platforms']}", number_style),
            Paragraph(format_change(metrics['platforms_change']), number_style)
        ]
    ]
    
    delivery_table = Table(delivery_table_data, colWidths=[1.5*inch, 1.5*inch, 1.5*inch, 1.2*inch])
    delivery_table.setStyle(TableStyle([
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
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('TOPPADDING', (0, 0), (-1, 0), 8),
    ]))
    story.append(delivery_table)
    story.append(Spacer(1, 10))

    # Add platform breakdown
    platform_text = "<b>Platform Breakdown:</b><br/>"
    for _, row in delivery_data['platform_breakdown'].iterrows():
        platform_text += f"• {row['طريقة الدفع']}: {row['العدد']} orders, SAR {row['المبلغ الصافي']:,.2f}<br/>"
    story.append(Paragraph(platform_text, platform_style))
    story.append(Spacer(1, 10))

    # Add Subscription Section
    story.append(Paragraph("Subscription Sales", section_style))
    story.append(Spacer(1, 10))
    
    # Create subscription table
    subscription_table_data = [
        # Overview Section
        ['Subscription Overview', 'Value'],
        ['Total Active Subscriptions', f"{subscription_data['total_subscriptions']:,}"],
        ['Total Revenue', format_currency(subscription_data['total_revenue'])],
        # New Subscriptions Section
        ['New Subscriptions', ''],
        ['Today', f"{subscription_data['new_users_today']}"],
        ['Yesterday', f"{subscription_data['new_users_yesterday']}"],
        ['Change vs Yesterday', Paragraph(f"<font color='{'green' if subscription_data['new_users_change'] >= 0 else 'red'}'>{subscription_data['new_users_change']:+.1f}%</font>", number_style)],
        # Revenue Analysis Section
        ['Revenue Analysis', ''],
        ['New Subscriptions Revenue', format_currency(subscription_data['metrics']['new_users_revenue'])],
        ['Average Value', format_currency(subscription_data['metrics']['avg_subscription_value'])]
    ]
    
    subscription_table = Table(subscription_table_data, colWidths=[2.5*inch, 2.5*inch])
    subscription_table.setStyle(TableStyle([
        # Base styles
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        # Section headers
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#D84B27')),
        ('BACKGROUND', (0, 3), (-1, 3), HexColor('#D84B27')),
        ('BACKGROUND', (0, 7), (-1, 7), HexColor('#D84B27')),
        # Header text
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('TEXTCOLOR', (0, 3), (-1, 3), colors.white),
        ('TEXTCOLOR', (0, 7), (-1, 7), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 3), (-1, 3), 'Helvetica-Bold'),
        ('FONTNAME', (0, 7), (-1, 7), 'Helvetica-Bold'),
        # Merge section header cells
        ('SPAN', (0, 3), (1, 3)),
        ('SPAN', (0, 7), (1, 7)),
        # Center all content
        ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
        ('ALIGN', (1, 1), (1, -1), 'CENTER'),
    ]))
    story.append(subscription_table)
    story.append(Spacer(1, 10))

    # Add subscription breakdown if needed
    if len(subscription_data['details']) > 0:
        sub_breakdown = "<b>Subscription Details:</b><br/>"
        sub_breakdown += f"• Total Active Subscriptions: {subscription_data['total_subscriptions']}<br/>"
        sub_breakdown += f"• New Subscriptions Today: {subscription_data['new_users_today']} "
        if subscription_data['new_users_change'] >= 0:
            sub_breakdown += f"(<font color='green'>+{subscription_data['new_users_change']:.1f}%</font> vs yesterday)<br/>"
        else:
            sub_breakdown += f"(<font color='red'>{subscription_data['new_users_change']:+.1f}%</font> vs yesterday)<br/>"
        sub_breakdown += f"• New Subscriptions Yesterday: {subscription_data['new_users_yesterday']}<br/>"
        sub_breakdown += f"• Revenue from New Subscriptions: SAR {subscription_data['metrics']['new_users_revenue']:,.2f}<br/>"
        sub_breakdown += f"• Total Revenue: SAR {subscription_data['total_revenue']:,.2f}<br/>"
        sub_breakdown += f"• Average Subscription Value: SAR {subscription_data['metrics']['avg_subscription_value']:,.2f}<br/><br/>"
        
        # Add plan distribution
        if subscription_data['metrics']['plan_distribution']:
            sub_breakdown += "<b>Plan Distribution:</b><br/>"
            for plan, count in subscription_data['metrics']['plan_distribution'].items():
                sub_breakdown += f"• {plan}: {count} ({count/subscription_data['total_subscriptions']*100:.1f}%)<br/>"
        
        # Add payment methods
        if subscription_data['metrics']['payment_methods']:
            sub_breakdown += "<br/><b>Payment Methods:</b><br/>"
            for method, count in subscription_data['metrics']['payment_methods'].items():
                sub_breakdown += f"• {method}: {count} ({count/subscription_data['total_subscriptions']*100:.1f}%)<br/>"
        
        story.append(Paragraph(sub_breakdown, platform_style))

    # Build PDF
    doc.build(story)

if __name__ == "__main__":
    generate_sales_report()
    print(f"\nSales report has been generated in reports directory") 