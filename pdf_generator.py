#!/usr/bin/env python3
"""
PDF Report Generator for Web3 News Articles
A clean, importable module for generating formatted PDF reports
"""

from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from bs4 import BeautifulSoup
import os


class Web3NewsPDFGenerator:
    """
    A clean PDF generator for Web3 news articles with proper formatting
    """
    
    def __init__(self, output_filename=None):
        """
        Initialize the PDF generator
        
        Args:
            output_filename (str): Optional custom filename. If None, generates timestamped filename
        """
        if output_filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            self.output_filename = f"web3_news_report_{timestamp}.pdf"
        else:
            self.output_filename = output_filename
            
        self.styles = getSampleStyleSheet()
        self._setup_styles()
    
    def _setup_styles(self):
        """Setup custom paragraph styles for professional formatting"""
        
        # Main source header (H1) - Blue, large, bold
        self.source_header_style = ParagraphStyle(
            'SourceHeader',
            parent=self.styles['Heading1'],
            fontSize=20,
            spaceAfter=15,
            spaceBefore=25,
            textColor=HexColor('#1E3A8A'),  # Blue
            fontName='Helvetica-Bold',
            alignment=TA_LEFT
        )
        
        # Article title (H2) - Purple, medium, bold
        self.title_style = ParagraphStyle(
            'ArticleTitle',
            parent=self.styles['Heading2'],
            fontSize=16,
            spaceAfter=10,
            spaceBefore=15,
            textColor=HexColor('#7C3AED'),  # Purple
            fontName='Helvetica-Bold',
            alignment=TA_LEFT
        )
        
        # Date style - Gray, smaller
        self.date_style = ParagraphStyle(
            'ArticleDate',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=5,
            spaceBefore=5,
            textColor=HexColor('#6B7280'),  # Gray
            fontName='Helvetica',
            alignment=TA_LEFT
        )
        
        # Link style - Orange, smaller, indented
        self.link_style = ParagraphStyle(
            'ArticleLink',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=8,
            spaceBefore=5,
            textColor=HexColor('#F59E0B'),  # Orange
            fontName='Helvetica',
            leftIndent=20,
            alignment=TA_LEFT
        )
        
        # Summary style - Black, readable, indented
        self.summary_style = ParagraphStyle(
            'ArticleSummary',
            parent=self.styles['Normal'],
            fontSize=12,
            spaceAfter=20,
            spaceBefore=8,
            textColor=HexColor('#1F2937'),  # Dark gray
            fontName='Helvetica',
            leftIndent=20,
            alignment=TA_LEFT,
            leading=16  # Line spacing
        )
        
        # Report title style - Large, centered
        self.report_title_style = ParagraphStyle(
            'ReportTitle',
            parent=self.styles['Title'],
            fontSize=26,
            spaceAfter=10,
            spaceBefore=20,
            textColor=HexColor('#111827'),  # Very dark gray
            fontName='Helvetica-Bold',
            alignment=TA_CENTER
        )
        
        # Report date style - Centered, smaller
        self.report_date_style = ParagraphStyle(
            'ReportDate',
            parent=self.styles['Normal'],
            fontSize=12,
            spaceAfter=25,
            spaceBefore=10,
            textColor=HexColor('#6B7280'),  # Gray
            fontName='Helvetica',
            alignment=TA_CENTER
        )
    
    def _clean_html(self, html_text):
        """Remove HTML tags and clean text"""
        if not html_text:
            return ""
        
        # Use BeautifulSoup to clean HTML
        soup = BeautifulSoup(html_text, 'html.parser')
        clean_text = soup.get_text()
        
        # Remove extra whitespace
        clean_text = ' '.join(clean_text.split())
        return clean_text
    
    def _format_source_name(self, source):
        """Format source name for display"""
        source_mapping = {
            'ethereum_blog': 'Ethereum Blog',
            'arbitrum_medium': 'Arbitrum Medium',
            'polygon_blog': 'Polygon Blog',
            'solana_news': 'Solana News',
            'flow_blog': 'Flow Blog'
        }
        return source_mapping.get(source, source.replace('_', ' ').title())
    
    def _format_date(self, date_string):
        """Format date string for display"""
        try:
            # Try to parse and format the date
            if 'GMT' in date_string:
                # Remove GMT and parse
                date_string = date_string.replace('GMT', '').strip()
            
            # Try different date formats
            for fmt in ['%a, %d %b %Y %H:%M:%S', '%Y-%m-%d', '%d %b %Y']:
                try:
                    parsed_date = datetime.strptime(date_string, fmt)
                    return parsed_date.strftime('%B %d, %Y')
                except ValueError:
                    continue
            
            # If all parsing fails, return original
            return date_string
        except:
            return date_string
    
    def generate_report(self, articles):
        """
        Generate PDF report from articles
        
        Args:
            articles (list): List of article dictionaries with keys:
                - source: Article source
                - title: Article title
                - link: Article URL
                - date: Publication date
                - summary: Article summary
        
        Returns:
            str: Path to generated PDF file
        """
        if not articles:
            raise ValueError("No articles provided for PDF generation")
        
        # Create PDF document
        doc = SimpleDocTemplate(
            self.output_filename,
            pagesize=A4,
            rightMargin=50,
            leftMargin=50,
            topMargin=50,
            bottomMargin=50
        )
        
        story = []
        
        # Add report header
        story.append(Paragraph("Web3 News Updates Report", self.report_title_style))
        story.append(Paragraph(f"Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}", self.report_date_style))
        story.append(Spacer(1, 20))
        
        # Group articles by source
        articles_by_source = {}
        for article in articles:
            source = article['source']
            if source not in articles_by_source:
                articles_by_source[source] = []
            articles_by_source[source].append(article)
        
        # Generate content for each source
        for source, source_articles in articles_by_source.items():
            # Add source header (H1)
            formatted_source = self._format_source_name(source)
            story.append(Paragraph(formatted_source, self.source_header_style))
            
            # Add articles for this source
            for article in source_articles:
                # Add title (H2)
                title = article.get('title', 'No Title')
                story.append(Paragraph(title, self.title_style))
                
                # Add date
                date = article.get('date', 'No Date')
                formatted_date = self._format_date(date)
                story.append(Paragraph(f"Published: {formatted_date}", self.date_style))
                
                # Add link
                link = article.get('link', 'No Link Available')
                story.append(Paragraph(f"Link: {link}", self.link_style))
                
                # Add summary
                summary = article.get('summary', 'No summary available')
                clean_summary = self._clean_html(summary)
                
                # Truncate summary if too long (keep it readable)
                if len(clean_summary) > 600:
                    clean_summary = clean_summary[:600] + "..."
                
                story.append(Paragraph(clean_summary, self.summary_style))
                
                # Add space between articles
                story.append(Spacer(1, 15))
            
            # Add page break between sources (if more than one source)
            if len(articles_by_source) > 1 and source != list(articles_by_source.keys())[-1]:
                story.append(PageBreak())
        
        # Build the PDF
        doc.build(story)
        
        return self.output_filename
    
    def generate_and_print_summary(self, articles):
        """
        Generate PDF and print a summary of the report
        
        Args:
            articles (list): List of article dictionaries
        
        Returns:
            str: Path to generated PDF file
        """
        try:
            pdf_path = self.generate_report(articles)
            
            print(f"\n✅ PDF report generated successfully!")
            print(f"📄 Report saved as: {pdf_path}")
            print(f"📊 Total articles in report: {len(articles)}")
            
            # Print summary by source
            print("\n📋 Report Summary:")
            articles_by_source = {}
            for article in articles:
                source = article['source']
                if source not in articles_by_source:
                    articles_by_source[source] = 0
                articles_by_source[source] += 1
            
            for source, count in articles_by_source.items():
                formatted_source = self._format_source_name(source)
                print(f"  • {formatted_source}: {count} articles")
            
            return pdf_path
            
        except Exception as e:
            print(f"❌ Error generating PDF: {e}")
            raise


# Convenience function for easy usage
def generate_news_pdf(articles, output_filename=None):
    """
    Convenience function to generate PDF report from articles
    
    Args:
        articles (list): List of article dictionaries
        output_filename (str): Optional custom filename
    
    Returns:
        str: Path to generated PDF file
    """
    generator = Web3NewsPDFGenerator(output_filename)
    return generator.generate_and_print_summary(articles)


# Example usage (for testing)
if __name__ == "__main__":
    # Sample data for testing
    sample_articles = [
        {
            'source': 'ethereum_blog',
            'title': 'Protocol Update 002 - Scale Blobs',
            'link': 'https://blog.ethereum.org/en/2025/08/22/protocol-update-002',
            'date': 'Fri, 22 Aug 2025 00:00:00 GMT',
            'summary': 'Following up from Protocol Update 001, we\'d like to introduce our approach to blob scaling. The L1 serves as a robust foundation for L2 systems to scale Ethereum, and a necessary component of secure L2 solutions is data availability provided by the L1.'
        },
        {
            'source': 'arbitrum_medium',
            'title': 'Most profitable SushiSwap liquidity pool ArbiFLUX-ETH — 162.44% APY',
            'link': 'https://arbitrum.medium.com/most-profitable-sushiswap-liquidity-pool-arbiflux-eth-162-44-apy-8b717e5e7b2d',
            'date': 'Wed, 15 Dec 2021 01:20:00 GMT',
            'summary': 'Just a month after launch, ArbiFLUX-ETH has become the most profitable APY pool on SushiSwap (Arbitrum Layer). So far there have been 1,222 ArbiFLUX high monetary velocity transfers.'
        }
    ]
    
    # Test the generator
    generate_news_pdf(sample_articles, "test_report.pdf")
