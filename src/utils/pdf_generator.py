from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor

def create_title_style():
    """Create title style for PDF"""
    return ParagraphStyle(
        'CustomTitle',
        fontName='Helvetica-Bold',
        fontSize=20,
        spaceAfter=15,
        alignment=1
    )

def create_section_style():
    """Create section style for PDF"""
    return ParagraphStyle(
        'Section',
        fontName='Helvetica-Bold',
        fontSize=12,
        spaceAfter=5,
        alignment=0
    )

def create_number_style():
    """Create number style for PDF"""
    return ParagraphStyle(
        'Number',
        fontName='Helvetica',
        fontSize=10,
        leading=12,
        alignment=1
    ) 