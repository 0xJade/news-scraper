#!/usr/bin/env python3
"""
News Scraper ETL Pipeline
A comprehensive pipeline for scraping blockchain news, generating AI proposals, 
creating PDF reports, and sending email notifications.
"""

import os
import json
from typing import List, Dict, Optional
from dotenv import load_dotenv

# Local imports
from _01_blockchain_news_scraper import BlockchainNewsScraper
from _02_pdf_generator import generate_enhanced_news_pdf
from _03_email_sender import EmailSender

# Third-party imports
import anthropic


class NewsScraperETL:
    """
    Main ETL pipeline class for blockchain news processing
    """
    
    def __init__(self):
        """Initialize the ETL pipeline with configuration"""
        # Load environment variables
        load_dotenv()
        
        # Validate required environment variables
        self._validate_environment()
        
        # Initialize components
        self.scraper = BlockchainNewsScraper()
        self.client = anthropic.Anthropic()
        self.sender = EmailSender()
        
        # Configuration
        self.api_key = os.getenv('ANTHROPIC_API_KEY')
        self.model = os.getenv('ANTHROPIC_MODEL')
        self.email_user = os.getenv('EMAIL_USER')

        if not self.email_user:
            raise ValueError("EMAIL_USER environment variable is required")
    
    def _validate_environment(self) -> None:
        """Validate that all required environment variables are set"""
        required_vars = ['ANTHROPIC_API_KEY', 'ANTHROPIC_MODEL', 'EMAIL_USER']
        missing_vars = [var for var in required_vars if not os.getenv(var)]
        
        if missing_vars:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
    
    def scrape_articles(self) -> List[Dict]:
        """
        Scrape blockchain news articles from configured sources
        
        Returns:
            List of article dictionaries
        """
        print("🔄 Step 1: Scraping blockchain news articles...")
        
        # Try to get Flow blog RSS feed
        flow_rss = self.scraper.get_flow_blog_rss()
        if flow_rss:
            print(f"✅ Found Flow blog RSS: {flow_rss}")
        
        # Scrape all configured sources
        articles = self.scraper.scrape_rss_feeds()
        
        if not articles:
            print("⚠️  No articles found during scraping")
            return []
        
        print(f"✅ Successfully scraped {len(articles)} articles")
        return articles
    
    def print_articles_summary(self, articles: List[Dict]) -> None:
        """Print a formatted summary of scraped articles"""
        print(f"\n{'='*60}")
        print("📰 SCRAPED ARTICLES SUMMARY")
        print(f"{'='*60}")
        
        for i, article in enumerate(articles, 1):
            print(f"\n{i}. Source: {article['source']}")
            print(f"   Title: {article['title']}")
            print(f"   Date: {article['date']}")
            print(f"   Link: {article['link']}")
            print(f"   Summary: {article['summary'][:100]}...")
            print("-" * 40)
    
    def generate_ai_proposals(self, articles: List[Dict]) -> List[Dict]:
        """
        Generate AI-powered research proposals for each article
        
        Args:
            articles: List of scraped articles
            
        Returns:
            List of articles with AI-generated proposals
        """
        print("\n Step 2: Generating AI research proposals...")
        
        if not articles:
            print("⚠️  No articles to process")
            return []
        
        processed_articles = []
        
        for i, article in enumerate(articles, 1):
            print(f"   Processing article {i}/{len(articles)}: {article['title'][:50]}...")
            
            summary = article.get('summary')
            if not summary:
                print(f"   ⚠️  No summary found for article {i}")
                processed_articles.append(article)
                continue
            
            try:
                # Generate AI proposal
                message = self.client.messages.create(
                    model=self.model,
                    max_tokens=1000,
                    messages=[
                        {
                            "role": "user",
                            "content": (
                                "As a research agency experienced in user research, "
                                "can you take the content of this article and generate "
                                f"a proposal idea to perform user research?: {summary}"
                            )
                        }
                    ]
                )
                
                # Update article with AI-generated proposal
                article['ai_proposal'] = message.content[0].text
                article['summary'] = message.content[0].text  # Replace summary with proposal
                
                print(f"   ✅ AI proposal generated for article {i}")
                
            except Exception as e:
                print(f"   ❌ Error generating AI proposal for article {i}: {e}")
                article['ai_proposal'] = "Error generating proposal"
            
            processed_articles.append(article)
        
        print(f"✅ Successfully processed {len(processed_articles)} articles with AI proposals")
        return processed_articles
    
    def generate_pdf_report(self, articles: List[Dict]) -> Optional[str]:
        """
        Generate PDF report from processed articles
        
        Args:
            articles: List of articles with AI proposals
            
        Returns:
            Path to generated PDF file, or None if failed
        """
        print("\n Step 3: Generating PDF report...")
        
        if not articles:
            print("⚠️  No articles to include in PDF")
            return None
        
        try:
            pdf_path = generate_enhanced_news_pdf(articles)
            print(f"✅ PDF report generated successfully: {pdf_path}")
            return pdf_path
            
        except Exception as e:
            print(f"❌ Error generating PDF report: {e}")
            return None
    
    def send_email_notification(self, pdf_path: str) -> bool:
        """
        Send email notification with PDF attachment
        
        Args:
            pdf_path: Path to the PDF file to attach
            
        Returns:
            True if email sent successfully, False otherwise
        """
        print("\n🔄 Step 4: Sending email notification...")
        
        if not pdf_path or not os.path.exists(pdf_path):
            print("❌ PDF file not found, cannot send email")
            return False
        
        try:
            # Use default recipients from .env file
            success = self.sender.send_to_default_recipients(
                subject="Blockchain News Research Proposals",
                message=(
                    "Hello! Please find attached the latest blockchain news "
                    "research proposals generated by our AI system.\n\n"
                    f"Total articles processed: {len(self.articles) if hasattr(self, 'articles') else 'Unknown'}"
                ),
                attachments=pdf_path
            )
            
            if success:
                print("✅ Email notification sent successfully!")
            else:
                print("❌ Failed to send email notification")
            
            return success
            
        except Exception as e:
            print(f"❌ Error sending email: {e}")
            return False
    
    def run_pipeline(self) -> bool:
        """
        Execute the complete ETL pipeline
        
        Returns:
            True if pipeline completed successfully, False otherwise
        """
        print(" Starting News Scraper ETL Pipeline...\n")
        
        try:
            # Step 1: Scrape articles
            self.articles = self.scrape_articles()
            if not self.articles:
                print("❌ Pipeline failed: No articles scraped")
                return False
            
            # Display summary
            self.print_articles_summary(self.articles)
            
            # Step 2: Generate AI proposals
            self.articles = self.generate_ai_proposals(self.articles)
            
            # Step 3: Generate PDF report
            pdf_path = self.generate_pdf_report(self.articles)
            if not pdf_path:
                print("❌ Pipeline failed: Could not generate PDF")
                return False
            
            # Step 4: Send email notification
            email_success = self.send_email_notification(pdf_path)
            
            print(f"\n{'='*60}")
            print(" PIPELINE COMPLETED SUCCESSFULLY!")
            print(f"{'='*60}")
            print(f" Articles processed: {len(self.articles)}")
            print(f"📄 PDF generated: {pdf_path}")
            print(f"📧 Email sent: {'✅ Yes' if email_success else '❌ No'}")
            
            return True
            
        except Exception as e:
            print(f"\n❌ Pipeline failed with error: {e}")
            return False


def main():
    """Main entry point for the ETL pipeline"""
    try:
        # Create and run pipeline
        pipeline = NewsScraperETL()
        success = pipeline.run_pipeline()
        
        if success:
            print("\n Pipeline completed successfully!")
        else:
            print("\n💥 Pipeline failed!")
            exit(1)
            
    except Exception as e:
        print(f"\n💥 Fatal error: {e}")
        exit(1)


if __name__ == "__main__":
    main()

