#!/usr/bin/env python3
"""
PDF Report Generator for Web3 News Articles
A clean, importable module for generating formatted PDF reports
"""

from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, KeepTogether
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
            fontSize=11,
            spaceAfter=20,
            spaceBefore=8,
            textColor=HexColor('#1F2937'),  # Dark gray
            fontName='Helvetica',
            leftIndent=20,
            alignment=TA_LEFT,
            leading=14  # Line spacing
        )
        
        # Long content style - For proposals and detailed content
        self.long_content_style = ParagraphStyle(
            'LongContent',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=12,
            spaceBefore=6,
            textColor=HexColor('#374151'),  # Medium gray
            fontName='Helvetica',
            leftIndent=25,
            alignment=TA_LEFT,
            leading=13,  # Tighter line spacing for long content
            firstLineIndent=0
        )
        
        # Section header style - For proposal sections
        self.section_header_style = ParagraphStyle(
            'SectionHeader',
            parent=self.styles['Heading3'],
            fontSize=13,
            spaceAfter=8,
            spaceBefore=15,
            textColor=HexColor('#059669'),  # Green
            fontName='Helvetica-Bold',
            alignment=TA_LEFT
        )
        
        # H4 header style
        self.h4_style = ParagraphStyle(
            'H4Header',
            parent=self.styles['Heading4'],
            fontSize=12,
            spaceAfter=6,
            spaceBefore=12,
            textColor=HexColor('#7C2D12'),  # Brown
            fontName='Helvetica-Bold',
            alignment=TA_LEFT
        )
        
        # List item style
        self.list_item_style = ParagraphStyle(
            'ListItem',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=4,
            spaceBefore=2,
            textColor=HexColor('#374151'),
            fontName='Helvetica',
            leftIndent=30,
            alignment=TA_LEFT,
            leading=12
        )
        
        # Numbered list style
        self.numbered_list_style = ParagraphStyle(
            'NumberedList',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=4,
            spaceBefore=2,
            textColor=HexColor('#374151'),
            fontName='Helvetica',
            leftIndent=30,
            alignment=TA_LEFT,
            leading=12
        )
        
        # Quote style
        self.quote_style = ParagraphStyle(
            'Quote',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=8,
            spaceBefore=8,
            textColor=HexColor('#6B7280'),
            fontName='Helvetica-Italic',
            leftIndent=40,
            rightIndent=20,
            alignment=TA_LEFT,
            leading=12,
            borderWidth=1,
            borderColor=HexColor('#D1D5DB'),
            borderPadding=8
        )
        
        # Code style
        self.code_style = ParagraphStyle(
            'Code',
            parent=self.styles['Normal'],
            fontSize=9,
            spaceAfter=2,
            spaceBefore=2,
            textColor=HexColor('#DC2626'),
            fontName='Courier',
            leftIndent=25,
            alignment=TA_LEFT,
            leading=11
        )
        
        # Enhanced proposal styles
        self.proposal_h2_style = ParagraphStyle(
            'ProposalH2',
            parent=self.styles['Heading2'],
            fontSize=16,
            spaceAfter=12,
            spaceBefore=20,
            textColor=HexColor('#FFFFFF'),  # White text
            fontName='Helvetica-Bold',
            alignment=TA_LEFT,
            backColor=HexColor('#059669'),  # Green background
            borderWidth=1,
            borderColor=HexColor('#047857'),
            borderPadding=8,
            leftIndent=10
        )
        
        self.proposal_h3_style = ParagraphStyle(
            'ProposalH3',
            parent=self.styles['Heading3'],
            fontSize=14,
            spaceAfter=8,
            spaceBefore=15,
            textColor=HexColor('#DC2626'),  # Red text
            fontName='Helvetica-Bold',
            alignment=TA_LEFT,
            leftIndent=15
        )
        
        self.executive_summary_style = ParagraphStyle(
            'ExecutiveSummary',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=15,
            spaceBefore=10,
            textColor=HexColor('#1E40AF'),  # Blue text
            fontName='Helvetica',
            alignment=TA_LEFT,
            leftIndent=20,
            rightIndent=20,
            leading=14,
            borderWidth=2,
            borderColor=HexColor('#3B82F6'),
            borderPadding=12,
            backColor=HexColor('#EFF6FF')  # Light blue background
        )
        
        self.objective_style = ParagraphStyle(
            'Objective',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=8,
            spaceBefore=6,
            textColor=HexColor('#166534'),  # Dark green text
            fontName='Helvetica',
            alignment=TA_LEFT,
            leftIndent=25,
            rightIndent=15,
            leading=13,
            borderWidth=1,
            borderColor=HexColor('#10B981'),
            borderPadding=8,
            backColor=HexColor('#F0FDF4')  # Light green background
        )
        
        self.enhanced_bullet_list_style = ParagraphStyle(
            'EnhancedBulletList',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=3,
            spaceBefore=2,
            textColor=HexColor('#374151'),
            fontName='Helvetica',
            leftIndent=35,
            alignment=TA_LEFT,
            leading=12,
            firstLineIndent=-15  # Hanging indent for bullets
        )
        
        self.enhanced_quote_style = ParagraphStyle(
            'EnhancedQuote',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=10,
            spaceBefore=8,
            textColor=HexColor('#4F46E5'),  # Indigo text
            fontName='Helvetica-Italic',
            leftIndent=30,
            rightIndent=25,
            alignment=TA_LEFT,
            leading=13,
            borderWidth=2,
            borderColor=HexColor('#6366F1'),
            borderPadding=10,
            backColor=HexColor('#EEF2FF')  # Light indigo background
        )
        
        self.methodology_style = ParagraphStyle(
            'Methodology',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=6,
            spaceBefore=4,
            textColor=HexColor('#7C2D12'),  # Brown text
            fontName='Helvetica',
            alignment=TA_LEFT,
            leftIndent=20,
            leading=13
        )
        
        self.deliverable_style = ParagraphStyle(
            'Deliverable',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=6,
            spaceBefore=4,
            textColor=HexColor('#9D174D'),  # Pink text
            fontName='Helvetica',
            alignment=TA_LEFT,
            leftIndent=20,
            leading=13
        )
        
        self.background_style = ParagraphStyle(
            'Background',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=8,
            spaceBefore=6,
            textColor=HexColor('#1E40AF'),  # Blue text
            fontName='Helvetica',
            alignment=TA_LEFT,
            leftIndent=20,
            leading=13
        )
        
        self.research_areas_style = ParagraphStyle(
            'ResearchAreas',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=6,
            spaceBefore=4,
            textColor=HexColor('#7C2D12'),  # Brown text
            fontName='Helvetica',
            alignment=TA_LEFT,
            leftIndent=20,
            leading=13
        )
        
        self.timeline_style = ParagraphStyle(
            'Timeline',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=6,
            spaceBefore=4,
            textColor=HexColor('#059669'),  # Green text
            fontName='Helvetica',
            alignment=TA_LEFT,
            leftIndent=20,
            leading=13
        )
        
        self.investment_style = ParagraphStyle(
            'Investment',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=6,
            spaceBefore=4,
            textColor=HexColor('#DC2626'),  # Red text
            fontName='Helvetica',
            alignment=TA_LEFT,
            leftIndent=20,
            leading=13
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
    

    
    def _parse_markdown(self, text):
        """Parse markdown content and convert to structured format for PDF"""
        if not text:
            return []
        
        elements = []
        lines = text.split('\n')
        current_paragraph = ""
        in_list = False
        
        for line in lines:
            original_line = line
            line = line.strip()
            
            # Empty line - end current paragraph
            if not line:
                if current_paragraph:
                    elements.append(('paragraph', current_paragraph.strip()))
                    current_paragraph = ""
                    in_list = False
                continue
            
            # Headers
            if line.startswith('#'):
                if current_paragraph:
                    elements.append(('paragraph', current_paragraph.strip()))
                    current_paragraph = ""
                
                # Count # to determine header level
                header_level = 0
                for char in line:
                    if char == '#':
                        header_level += 1
                    else:
                        break
                
                header_text = line[header_level:].strip()
                elements.append(('header', header_text, header_level))
                continue
            
            # Bold text (markdown **text** or __text__)
            if '**' in line or '__' in line:
                line = self._process_bold_text(line)
            
            # Italic text (markdown *text* or _text_)
            if '*' in line or '_' in line:
                line = self._process_italic_text(line)
            
            # Code blocks (markdown `code`)
            if '`' in line:
                line = self._process_code_text(line)
            
            # Lists
            if line.startswith(('- ', '* ', '+ ')):
                if current_paragraph:
                    elements.append(('paragraph', current_paragraph.strip()))
                    current_paragraph = ""
                
                # Handle nested lists
                indent_level = len(original_line) - len(original_line.lstrip())
                list_text = line[2:].strip()  # Remove bullet and space
                elements.append(('list_item', list_text, indent_level))
                in_list = True
                continue
            
            # Numbered lists
            if line and line[0].isdigit() and '. ' in line[:5]:
                if current_paragraph:
                    elements.append(('paragraph', current_paragraph.strip()))
                    current_paragraph = ""
                
                # Extract number and text
                parts = line.split('. ', 1)
                if len(parts) == 2:
                    number = parts[0]
                    list_text = parts[1].strip()
                    elements.append(('numbered_list', list_text, number))
                    in_list = True
                    continue
            
            # Blockquotes
            if line.startswith('> '):
                if current_paragraph:
                    elements.append(('paragraph', current_paragraph.strip()))
                    current_paragraph = ""
                
                quote_text = line[2:].strip()
                elements.append(('quote', quote_text))
                continue
            
            # Horizontal rules
            if line in ['---', '***', '___']:
                if current_paragraph:
                    elements.append(('paragraph', current_paragraph.strip()))
                    current_paragraph = ""
                elements.append(('hr', ''))
                continue
            
            # Regular text
            if current_paragraph:
                current_paragraph += " " + line
            else:
                current_paragraph = line
        
        # Add any remaining paragraph
        if current_paragraph:
            elements.append(('paragraph', current_paragraph.strip()))
        
        return elements
    
    def _process_bold_text(self, text):
        """Process bold markdown text"""
        # Replace **text** or ****text**** with <b>text</b> for reportlab
        import re
        # Handle 4 asterisks (****text****)
        text = re.sub(r'\*\*\*\*(.*?)\*\*\*\*', r'<b>\1</b>', text)
        # Handle 2 asterisks (**text**)
        text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
        # Handle double underscores (__text__)
        text = re.sub(r'__(.*?)__', r'<b>\1</b>', text)
        return text
    
    def _process_italic_text(self, text):
        """Process italic markdown text"""
        # Replace *text* with <i>text</i> for reportlab
        import re
        # Be careful not to replace bold markers - only single asterisks
        text = re.sub(r'(?<!\*)\*([^*]+)\*(?!\*)', r'<i>\1</i>', text)
        text = re.sub(r'(?<!_)_([^_]+)_(?!_)', r'<i>\1</i>', text)
        return text
    
    def _process_code_text(self, text):
        """Process inline code markdown text"""
        # Replace `code` with <code>code</code> for reportlab
        import re
        text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)
        return text
    
    def _detect_section_type(self, text):
        """Detect special section types for enhanced styling"""
        text_lower = text.lower().strip()
        
        # Executive summary detection
        if any(keyword in text_lower for keyword in ['executive summary', 'executive overview', 'summary']):
            return 'executive_summary'
        
        # Background & opportunity detection
        if any(keyword in text_lower for keyword in ['background', 'opportunity', 'context', 'overview']):
            return 'background'
        
        # Objectives detection
        if any(keyword in text_lower for keyword in ['objectives', 'goals', 'aims', 'targets', 'primary objective', 'secondary objective']):
            return 'objective'
        
        # Methodology detection
        if any(keyword in text_lower for keyword in ['methodology', 'approach', 'methods', 'process', 'phases', 'phase']):
            return 'methodology'
        
        # Research areas detection
        if any(keyword in text_lower for keyword in ['research areas', 'focus areas', 'key areas', 'research focus']):
            return 'research_areas'
        
        # Timeline detection
        if any(keyword in text_lower for keyword in ['timeline', 'schedule', 'milestones', 'deadlines']):
            return 'timeline'
        
        # Investment detection
        if any(keyword in text_lower for keyword in ['investment', 'budget', 'cost', 'funding', 'financial']):
            return 'investment'
        
        # Deliverables detection
        if any(keyword in text_lower for keyword in ['deliverables', 'outputs', 'results', 'outcomes', 'deliverable']):
            return 'deliverable'
        
        # Research questions
        if any(keyword in text_lower for keyword in ['research questions', 'questions', 'key questions']):
            return 'research_questions'
        
        # Target participants
        if any(keyword in text_lower for keyword in ['participants', 'target', 'audience', 'users', 'segments']):
            return 'participants'
        
        return 'general'
    
    def _process_markdown_text(self, text):
        """Enhanced markdown text processing with better formatting"""
        if not text:
            return text
        
        # Process bold text
        text = self._process_bold_text(text)
        
        # Process italic text
        text = self._process_italic_text(text)
        
        # Process code text
        text = self._process_code_text(text)
        
        # Process links (basic)
        import re
        text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<link href="\2">\1</link>', text)
        
        return text
    
    def _parse_markdown_enhanced(self, text):
        """Enhanced markdown parsing with section detection and better structure"""
        if not text:
            return []
        
        # Fix escape sequences first
        text = text.replace('\\n', '\n')  # Convert \n to actual newlines
        text = text.replace('\\t', '\t')  # Convert \t to actual tabs
        
        elements = []
        lines = text.split('\n')
        current_paragraph = ""
        
        for i, line in enumerate(lines):
            original_line = line
            line = line.strip()
            
            # Empty line - end current paragraph
            if not line:
                if current_paragraph:
                    processed_text = self._process_markdown_text(current_paragraph.strip())
                    section_type = self._detect_section_type(current_paragraph.strip())
                    elements.append(('paragraph', processed_text, section_type))
                    current_paragraph = ""
                continue
            
            # Headers - check for # at the beginning
            if line.startswith('#'):
                if current_paragraph:
                    processed_text = self._process_markdown_text(current_paragraph.strip())
                    section_type = self._detect_section_type(current_paragraph.strip())
                    elements.append(('paragraph', processed_text, section_type))
                    current_paragraph = ""
                
                # Count # to determine header level
                header_level = 0
                for char in line:
                    if char == '#':
                        header_level += 1
                    else:
                        break
                
                header_text = line[header_level:].strip()
                section_type = self._detect_section_type(header_text)
                elements.append(('header', header_text, header_level, section_type))
                continue
            
            # Improved list detection with regex
            import re
            
            # For bullet lists
            if re.match(r'^[\-\*\+]\s+', line):
                if current_paragraph:
                    processed_text = self._process_markdown_text(current_paragraph.strip())
                    section_type = self._detect_section_type(current_paragraph.strip())
                    elements.append(('paragraph', processed_text, section_type))
                    current_paragraph = ""
                
                # Handle nested lists
                indent_level = len(original_line) - len(original_line.lstrip())
                list_text = line[2:].strip()  # Remove bullet and space
                processed_text = self._process_markdown_text(list_text)
                elements.append(('list_item', processed_text, indent_level))
                continue
            
            # For numbered lists  
            if re.match(r'^\d+\.\s+', line):
                if current_paragraph:
                    processed_text = self._process_markdown_text(current_paragraph.strip())
                    section_type = self._detect_section_type(current_paragraph.strip())
                    elements.append(('paragraph', processed_text, section_type))
                    current_paragraph = ""
                
                # Extract number and text
                parts = line.split('. ', 1)
                if len(parts) == 2:
                    number = parts[0]
                    list_text = parts[1].strip()
                    processed_text = self._process_markdown_text(list_text)
                    elements.append(('numbered_list', processed_text, number))
                    continue
            
            # Blockquotes
            if line.startswith('> '):
                if current_paragraph:
                    processed_text = self._process_markdown_text(current_paragraph.strip())
                    section_type = self._detect_section_type(current_paragraph.strip())
                    elements.append(('paragraph', processed_text, section_type))
                    current_paragraph = ""
                
                quote_text = line[2:].strip()
                processed_text = self._process_markdown_text(quote_text)
                elements.append(('quote', processed_text))
                continue
            
            # Horizontal rules
            if line in ['---', '***', '___']:
                if current_paragraph:
                    processed_text = self._process_markdown_text(current_paragraph.strip())
                    section_type = self._detect_section_type(current_paragraph.strip())
                    elements.append(('paragraph', processed_text, section_type))
                    current_paragraph = ""
                elements.append(('hr', ''))
                continue
            
            # Regular text - accumulate into paragraph
            if current_paragraph:
                current_paragraph += " " + line
            else:
                current_paragraph = line
        
        # Add any remaining paragraph
        if current_paragraph:
            processed_text = self._process_markdown_text(current_paragraph.strip())
            section_type = self._detect_section_type(current_paragraph.strip())
            elements.append(('paragraph', processed_text, section_type))
        
        return elements
    
    def _create_table_of_contents(self, elements):
        """Create a table of contents from header elements"""
        toc_elements = []
        toc_elements.append(Paragraph("📋 Table of Contents", self.report_title_style))
        toc_elements.append(Spacer(1, 15))
        
        for element in elements:
            if element[0] == 'header':
                header_text = element[1]
                header_level = element[2]
                
                # Create indented TOC entry
                indent = "&nbsp;" * (header_level - 1) * 4
                toc_text = f"{indent}• {header_text}"
                
                if header_level == 1:
                    toc_elements.append(Paragraph(toc_text, self.title_style))
                elif header_level == 2:
                    toc_elements.append(Paragraph(toc_text, self.section_header_style))
                else:
                    toc_elements.append(Paragraph(toc_text, self.long_content_style))
        
        toc_elements.append(Spacer(1, 20))
        toc_elements.append(PageBreak())
        return toc_elements
    
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
        
        # Add report header with enhanced metadata
        story.append(Paragraph("📰 Web3 News Updates Report", self.report_title_style))
        story.append(Paragraph(f"🕒 Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}", self.report_date_style))
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
                
                # Check if content is structured markdown
                is_structured = (len(summary) > 500 or 
                               summary.count('#') > 2 or 
                               summary.count('**') > 3 or 
                               summary.count('- ') > 3 or
                               '\\n' in summary)
                
                if is_structured:
                    # Parse and format as enhanced markdown
                    markdown_elements = self._parse_markdown_enhanced(summary)
                    
                    # Create table of contents for long proposals
                    if len(markdown_elements) > 10:
                        toc_elements = self._create_table_of_contents(markdown_elements)
                        story.extend(toc_elements)
                    
                    # Group elements for better page breaks
                    current_section = []
                    
                    for element in markdown_elements:
                        if element[0] == 'paragraph':
                            if element[1]:  # Only add non-empty paragraphs
                                section_type = element[2]
                                if section_type == 'executive_summary':
                                    story.append(Paragraph(element[1], self.executive_summary_style))
                                elif section_type == 'objective':
                                    story.append(Paragraph(element[1], self.objective_style))
                                elif section_type == 'methodology':
                                    story.append(Paragraph(element[1], self.methodology_style))
                                elif section_type == 'deliverable':
                                    story.append(Paragraph(element[1], self.deliverable_style))
                                elif section_type == 'background':
                                    story.append(Paragraph(element[1], self.background_style))
                                elif section_type == 'research_areas':
                                    story.append(Paragraph(element[1], self.research_areas_style))
                                elif section_type == 'timeline':
                                    story.append(Paragraph(element[1], self.timeline_style))
                                elif section_type == 'investment':
                                    story.append(Paragraph(element[1], self.investment_style))
                                else:
                                    story.append(Paragraph(element[1], self.long_content_style))
                                
                                current_section.append(Paragraph(element[1], self.long_content_style))
                                
                        elif element[0] == 'header':
                            header_text = element[1]
                            header_level = element[2]
                            section_type = element[3]
                            
                            # Use enhanced styling for H2 headers
                            if header_level == 1:
                                story.append(Paragraph(header_text, self.title_style))
                            elif header_level == 2:
                                story.append(Paragraph(header_text, self.proposal_h2_style))
                            elif header_level == 3:
                                story.append(Paragraph(header_text, self.proposal_h3_style))
                            else:
                                story.append(Paragraph(header_text, self.h4_style))
                            
                            # Keep sections together
                            if current_section:
                                story.append(KeepTogether(current_section))
                                current_section = []
                                
                        elif element[0] == 'list_item':
                            list_text = element[1]
                            indent_level = element[2]
                            bullet = "• "
                            story.append(Paragraph(f"{bullet}{list_text}", self.enhanced_bullet_list_style))
                            
                        elif element[0] == 'numbered_list':
                            list_text = element[1]
                            number = element[2]
                            story.append(Paragraph(f"{number}. {list_text}", self.numbered_list_style))
                            
                        elif element[0] == 'quote':
                            quote_text = element[1]
                            story.append(Paragraph(f"💬 {quote_text}", self.enhanced_quote_style))
                            
                        elif element[0] == 'hr':
                            story.append(Spacer(1, 10))
                            story.append(Paragraph("─" * 60, self.long_content_style))
                            story.append(Spacer(1, 10))
                    
                    # Keep any remaining section together
                    if current_section:
                        story.append(KeepTogether(current_section))
                        
                else:
                    # Regular summary - truncate if too long
                    if len(summary) > 600:
                        summary = summary[:600] + "..."
                    story.append(Paragraph(summary, self.summary_style))
                
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


# Enhanced convenience function for proposal content
def generate_enhanced_news_pdf(articles, output_filename=None):
    """
    Enhanced convenience function for generating PDF reports with better markdown support
    
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
            'source': 'claude_proposal',
            'title': 'User Research Proposal: Improving Ethereum User Experience',
            'link': 'Generated by Claude AI',
            'date': 'Generated on ' + datetime.now().strftime('%B %d, %Y'),
            'summary': '''# User Research Proposal: Improving Ethereum User Experience\\n\\n## Background & Opportunity\\n\\nThe integration of Arbitrum One Layer 2 scaling solution has created new opportunities for Ethereum ecosystem growth. This proposal outlines a comprehensive user research initiative to support Ethereum\'s ****"Improve UX"**** strategic track.\\n\\n## Executive Summary\\n\\nThis proposal outlines a comprehensive user research initiative to support Ethereum\'s ****"Improve UX"**** strategic track. The research will identify key pain points, barriers, and opportunities to create a more seamless, secure, and permissionless experience across the Ethereum ecosystem.\\n\\n> *"The goal is to make Ethereum as easy to use as traditional web applications while maintaining its core principles."*\\n\\n## Research Objectives\\n\\n****Primary Objective:**** Understand how to make Ethereum more accessible and user-friendly while maintaining its core principles of decentralization and security.\\n\\n****Secondary Objectives:****\\n- Map the current user journey across different Ethereum touchpoints\\n- Identify friction points that prevent mainstream adoption\\n- Understand security concerns and how they impact user behavior\\n- Explore mental models around permissionless systems\\n- Benchmark UX expectations against traditional web/financial services\\n\\n## Research Questions\\n\\n### Core Questions:\\n1. What are the primary barriers preventing users from adopting Ethereum-based applications?\\n2. How do users currently conceptualize and interact with decentralized systems?\\n3. What security vs. usability trade-offs are users willing to make?\\n4. Where do users experience the most friction in their Ethereum journey?\\n\\n### Supporting Questions:\\n- How do different user segments (crypto-native vs. newcomers) experience Ethereum differently?\\n- What language, terminology, and mental models resonate with users?\\n- How do users currently manage keys, wallets, and transactions?\\n- What are user expectations for transaction speed, cost, and reliability?\\n\\n---\\n\\n## Proposed Methodology\\n\\n### Phase 1: Foundation Research (4-6 weeks)\\n- ****Stakeholder interviews**** with Protocol team members and ecosystem partners\\n- ****Secondary research**** analysis of existing UX studies in crypto/blockchain\\n- ****Competitive analysis**** of user experiences in traditional and crypto applications\\n\\n### Phase 2: User Discovery (6-8 weeks)\\n- ****In-depth interviews**** (n=30-40) with diverse user segments:\\n  - Crypto newcomers/never-users\\n  - Occasional users\\n  - Power users/developers\\n  - Users who abandoned Ethereum\\n- ****Journey mapping sessions**** to understand end-to-end experiences\\n- ****Diary studies**** to capture real-world usage patterns over time\\n\\n### Phase 3: Experience Evaluation (4-6 weeks)\\n- ****Usability testing**** of key user flows across popular Ethereum applications\\n- ****Card sorting exercises**** to understand user mental models\\n- ****Prototype testing**** of potential UX improvements\\n\\n### Phase 4: Validation & Strategy (3-4 weeks)\\n- ****Survey research**** (n=500+) to validate findings at scale\\n- ****Workshop sessions**** with Protocol team to prioritize opportunities\\n- ****Roadmap development**** for UX improvements\\n\\n## Target Participants\\n\\n### Primary Segments:\\n- ****Crypto Curious**** (40%): Users interested in crypto but haven\'t used Ethereum\\n- ****Ethereum Beginners**** (30%): Users with <1 year of Ethereum experience\\n- ****Intermediate Users**** (20%): Regular Ethereum users (1-3 years experience)\\n- ****Advanced Users**** (10%): Power users, developers, and long-time participants\\n\\n### Demographic Considerations:\\n- Geographic diversity (North America, Europe, Asia, emerging markets)\\n- Age ranges (18-65+)\\n- Technical background variety\\n- Income/economic status diversity\\n\\n## Key Focus Areas\\n\\n1. ****Wallet and Key Management****\\n   - Setup and onboarding experiences\\n   - Security practices and concerns\\n   - Recovery and backup processes\\n\\n2. ****Transaction Experience****\\n   - Gas fee comprehension and prediction\\n   - Transaction status and confirmation\\n   - Error handling and recovery\\n\\n3. ****DApp Discovery and Usage****\\n   - How users find and evaluate applications\\n   - Cross-application experiences\\n   - Trust and security assessment\\n\\n4. ****Education and Support****\\n   - Learning resources and preferences\\n   - Community support utilization\\n   - Help-seeking behavior\\n\\n## Technical Implementation\\n\\nThe research will focus on key technical areas including:\\n\\n- `wallet.connect()` integration patterns\\n- Gas estimation algorithms\\n- Transaction confirmation flows\\n- Error handling mechanisms\\n\\n## Deliverables\\n\\n1. ****Comprehensive Research Report**** including:\\n   - Executive summary with key insights\\n   - Detailed findings by research phase\\n   - User personas and journey maps\\n   - Prioritized opportunity areas\\n\\n2. ****UX Strategy Roadmap**** featuring:\\n   - Short, medium, and long-term recommendations\\n   - Impact vs. effort prioritization matrix\\n   - Success metrics and KPIs\\n\\n3. ****Design Principles & Guidelines**** for:\\n   - Ethereum UX best practices\\n   - Language and terminology standards'''
        }
    ]
    
    # Test the enhanced generator
    print("Testing enhanced PDF generator with markdown content...")
    generate_enhanced_news_pdf(sample_articles, "enhanced_test_report.pdf")
