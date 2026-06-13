#!/usr/bin/env python3
"""
Generate PDF report from Markdown with embedded visualizations.
"""

import os
from pathlib import Path
import markdown
from weasyprint import HTML, CSS
from markdown.extensions.toc import TocExtension
from markdown.extensions.tables import TableExtension

def generate_pdf_report():
    """Convert Markdown report to PDF with styling."""
    
    # Paths
    base_path = Path(r"C:\dev\deixis\deixis_analysis_pipeline\yoruba_cross_linguistic_analysis")
    md_file = base_path / "Yoruba_Deixis_Analysis_Report.md"
    pdf_file = base_path / "Yoruba_Deixis_Analysis_Report.pdf"
    
    # Read markdown content
    with open(md_file, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    # Replace relative image paths with absolute paths
    viz_path = base_path / "visualizations"
    md_content = md_content.replace('visualizations/', f'file:///{viz_path}/')
    
    # Convert markdown to HTML
    md = markdown.Markdown(extensions=[
        'fenced_code',
        'tables',
        'toc',
        'nl2br',
        'sane_lists',
        'codehilite'
    ])
    
    html_content = md.convert(md_content)
    
    # Create full HTML document
    html_template = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Yoruba Deixis Analysis Report</title>
        <style>
            @page {{
                size: A4;
                margin: 2.5cm;
                @bottom-center {{
                    content: counter(page) " of " counter(pages);
                }}
            }}
            
            body {{
                font-family: Georgia, 'Times New Roman', serif;
                font-size: 11pt;
                line-height: 1.6;
                color: #333;
                max-width: 100%;
                margin: 0;
                padding: 0;
            }}
            
            h1 {{
                font-size: 24pt;
                color: #1a1a1a;
                margin-top: 0;
                page-break-before: always;
                border-bottom: 3px solid #E63946;
                padding-bottom: 10px;
            }}
            
            h1:first-child {{
                page-break-before: avoid;
            }}
            
            h2 {{
                font-size: 18pt;
                color: #2E86AB;
                margin-top: 30px;
                border-bottom: 1px solid #ddd;
                padding-bottom: 5px;
            }}
            
            h3 {{
                font-size: 14pt;
                color: #444;
                margin-top: 20px;
            }}
            
            h4 {{
                font-size: 12pt;
                color: #666;
                margin-top: 15px;
            }}
            
            p {{
                text-align: justify;
                margin: 10px 0;
            }}
            
            img {{
                max-width: 100%;
                height: auto;
                display: block;
                margin: 20px auto;
                page-break-inside: avoid;
            }}
            
            .figure-caption {{
                text-align: center;
                font-style: italic;
                color: #666;
                font-size: 10pt;
                margin: 10px 20px 20px 20px;
            }}
            
            table {{
                border-collapse: collapse;
                width: 100%;
                margin: 20px 0;
                font-size: 10pt;
                page-break-inside: avoid;
            }}
            
            th, td {{
                border: 1px solid #ddd;
                padding: 8px;
                text-align: left;
            }}
            
            th {{
                background-color: #f4f4f4;
                font-weight: bold;
            }}
            
            blockquote {{
                border-left: 4px solid #E63946;
                margin: 20px 0;
                padding: 10px 20px;
                background-color: #f9f9f9;
                font-style: italic;
            }}
            
            code {{
                background-color: #f4f4f4;
                padding: 2px 4px;
                font-family: 'Courier New', monospace;
                font-size: 10pt;
            }}
            
            pre {{
                background-color: #f4f4f4;
                padding: 10px;
                overflow-x: auto;
                font-family: 'Courier New', monospace;
                font-size: 9pt;
                line-height: 1.4;
                page-break-inside: avoid;
            }}
            
            ul, ol {{
                margin: 10px 0;
                padding-left: 30px;
            }}
            
            li {{
                margin: 5px 0;
            }}
            
            strong {{
                color: #1a1a1a;
            }}
            
            .key-findings {{
                background-color: #f0f8ff;
                border: 2px solid #2E86AB;
                border-radius: 5px;
                padding: 15px;
                margin: 20px 0;
                page-break-inside: avoid;
            }}
            
            .toc {{
                background-color: #f9f9f9;
                border: 1px solid #ddd;
                padding: 20px;
                margin: 20px 0;
                page-break-after: always;
            }}
            
            hr {{
                border: none;
                border-top: 1px solid #ddd;
                margin: 30px 0;
            }}
            
            /* Fix image captions */
            img + em {{
                display: block;
                text-align: center;
                font-style: italic;
                color: #666;
                font-size: 10pt;
                margin: -10px 20px 20px 20px;
            }}
        </style>
    </head>
    <body>
        {html_content}
    </body>
    </html>
    """
    
    # Generate PDF
    print("Generating PDF report...")
    try:
        HTML(string=html_template).write_pdf(pdf_file)
        print(f"PDF report saved to: {pdf_file}")
        
        # Also save HTML version for debugging
        html_file = base_path / "Yoruba_Deixis_Analysis_Report.html"
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_template)
        print(f"HTML report saved to: {html_file}")
        
    except Exception as e:
        print(f"Error generating PDF: {e}")
        print("Make sure WeasyPrint is installed: pip install weasyprint")

if __name__ == "__main__":
    generate_pdf_report()