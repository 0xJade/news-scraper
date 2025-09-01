#!/usr/bin/env python3
"""
Blockchain News Scraper Module
A clean, importable module for scraping blockchain news from RSS feeds
"""

import requests
from bs4 import BeautifulSoup
import feedparser
import time
from datetime import datetime
import logging

# Set up logging for better debugging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class BlockchainNewsScraper:
    """
    A clean news scraper for blockchain RSS feeds with proper error handling and logging
    """
    
    def __init__(self):
        self.sources = {
            'ethereum_blog': 'https://blog.ethereum.org/feed.xml',
            'arbitrum_medium': 'https://medium.com/feed/@arbitrum',
            # 'polygon_blog': 'https://blog.polygon.technology/feed',
            # 'solana_news': 'https://solana.com/news/rss.xml',
            # 'flow_blog': 'https://www.onflow.org/post/rss.xml'
        }
        
        # Add headers to mimic a real browser
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'application/rss+xml, application/xml, text/xml, application/atom+xml',
            'Accept-Language': 'en-US,en;q=0.9',
        }
    
    def test_url_accessibility(self, url, source_name):
        """Test if URL is accessible and what type of content it returns"""
        logger.info(f"Testing URL accessibility for {source_name}: {url}")
        
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            
            logger.info(f"{source_name} - Status Code: {response.status_code}")
            logger.info(f"{source_name} - Content-Type: {response.headers.get('content-type', 'Unknown')}")
            logger.info(f"{source_name} - Content Length: {len(response.content)} bytes")
            
            # Check if it's actually RSS/XML content
            content_type = response.headers.get('content-type', '').lower()
            is_xml = 'xml' in content_type or 'rss' in content_type or 'atom' in content_type
            
            if not is_xml:
                # Check if content starts with XML declaration or RSS tags
                content_preview = response.text[:200]
                logger.info(f"{source_name} - Content preview: {content_preview}")
                
                if not any(tag in content_preview.lower() for tag in ['<rss', '<feed', '<?xml']):
                    logger.warning(f"{source_name} - This appears to be HTML, not RSS/XML!")
            
            return response.status_code == 200, response
            
        except requests.exceptions.RequestException as e:
            logger.error(f"{source_name} - Request failed: {e}")
            return False, None
    
    def analyze_feed_structure(self, feed, source_name):
        """Analyze the feed structure to understand what's available"""
        logger.info(f"Analyzing feed structure for {source_name}")
        
        if feed.entries:
            # Analyze first entry structure
            first_entry = feed.entries[0]
        
        # Check for parsing errors
        if hasattr(feed, 'bozo') and feed.bozo:
            logger.warning(f"{source_name} - Feed has parsing issues: {feed.bozo_exception}")
    
    def scrape_rss_feeds(self):
        """
        Scrape RSS feeds from configured sources
        
        Returns:
            list: List of article dictionaries with keys:
                - source: Article source
                - title: Article title
                - link: Article URL
                - date: Publication date
                - summary: Article summary
        """
        articles = []
        
        for source, url in self.sources.items():
            logger.info(f"\n{'='*50}")
            logger.info(f"Processing source: {source}")
            logger.info(f"URL: {url}")
            
            try:
                # First, test URL accessibility
                is_accessible, response = self.test_url_accessibility(url, source)
                
                if not is_accessible:
                    logger.error(f"Skipping {source} - URL not accessible")
                    continue
                
                # Parse the feed
                logger.info(f"Parsing feed for {source}...")
                feed = feedparser.parse(url)
                
                # Analyze feed structure
                self.analyze_feed_structure(feed, source)
                
                # Check if feed has entries
                if len(feed.entries) > 0:
                    logger.info(f"Processing {len(feed.entries)} entries from {source}")
                    
                    for i, entry in enumerate(feed.entries[:3]):  # Latest 3 articles
                        logger.debug(f"Processing entry {i+1} from {source}: {getattr(entry, 'title', 'No title')}")
                        
                        # Check if entry has required fields
                        title = getattr(entry, 'title', 'No title')
                        summary = getattr(entry, 'summary', getattr(entry, 'description', ''))
                        
                        if self.is_upgrade_related(title + " " + summary):
                            article = {
                                'source': source,
                                'title': title,
                                'link': getattr(entry, 'link', ''),
                                'date': getattr(entry, 'published', getattr(entry, 'updated', 'No date')),
                                'summary': summary
                            }
                            articles.append(article)
                            logger.info(f"Added upgrade-related article from {source}: {title}")
                
                else:
                    logger.warning(f"No entries found in feed for {source}")
                    # Print more detailed feed information for debugging
                    if hasattr(feed, 'bozo') and feed.bozo:
                        logger.error(f"Feed parsing error for {source}: {feed.bozo_exception}")
                    
                    # Show raw content preview if feed is empty
                    if response:
                        logger.info(f"Raw content preview for {source}:")
                        logger.info(response.text[:500] + "..." if len(response.text) > 500 else response.text)
                
            except Exception as e:
                logger.error(f"Error scraping {source}: {e}")
                import traceback
                logger.error(traceback.format_exc())
        
        logger.info(f"\n{'='*50}")
        logger.info(f"Total articles found: {len(articles)}")
        return articles
    
    def is_upgrade_related(self, text):
        """
        Check if text contains upgrade-related keywords
        
        Args:
            text (str): Text to check for keywords
            
        Returns:
            bool: True if text contains upgrade-related keywords
        """
        keywords = ['upgrade', 'update', 'fork', 'hardfork', 'testnet', 
                   'mainnet', 'release', 'version', 'protocol', 'network']
        return any(keyword.lower() in text.lower() for keyword in keywords)
    
    def get_flow_blog_rss(self):
        """Special handler for Flow blog since it doesn't have RSS"""
        logger.info("Attempting to find RSS feed for Flow blog...")
        
        try:
            response = requests.get('https://flow.com/blog', headers=self.headers)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Look for RSS link in HTML head
            rss_link = soup.find('link', {'type': 'application/rss+xml'})
            if rss_link:
                rss_url = rss_link.get('href')
                logger.info(f"Found RSS feed for Flow: {rss_url}")
                return rss_url
            else:
                logger.warning("No RSS feed found for Flow blog")
                return None
                
        except Exception as e:
            logger.error(f"Error finding Flow RSS feed: {e}")
            return None
    
    def add_source(self, name, url):
        """
        Add a new RSS source to the scraper
        
        Args:
            name (str): Source name
            url (str): RSS feed URL
        """
        self.sources[name] = url
        logger.info(f"Added new source: {name} -> {url}")
    
    def remove_source(self, name):
        """
        Remove a source from the scraper
        
        Args:
            name (str): Source name to remove
        """
        if name in self.sources:
            del self.sources[name]
            logger.info(f"Removed source: {name}")
        else:
            logger.warning(f"Source {name} not found in sources")
    
    def get_sources(self):
        """
        Get current sources configuration
        
        Returns:
            dict: Current sources dictionary
        """
        return self.sources.copy()


# Convenience function for easy usage
def scrape_blockchain_news(max_articles_per_source=3):
    """
    Convenience function to scrape blockchain news
    
    Args:
        max_articles_per_source (int): Maximum articles to fetch per source
        
    Returns:
        list: List of article dictionaries
    """
    scraper = BlockchainNewsScraper()
    
    # Optional: Try to find Flow's actual RSS feed
    flow_rss = scraper.get_flow_blog_rss()
    if flow_rss:
        scraper.add_source('flow_blog', flow_rss)
    
    articles = scraper.scrape_rss_feeds()
    
    # Print results summary
    print(f"\n{'='*60}")
    print("FINAL RESULTS SUMMARY")
    print(f"{'='*60}")
    
    if articles:
        for article in articles:
            print(f"\nSource: {article['source']}")
            print(f"Title: {article['title']}")
            print(f"Date: {article['date']}")
            print(f"Link: {article['link']}")
            print("-" * 40)
    else:
        print("No upgrade-related articles found.")
    
    return articles


# Example usage (for testing)
if __name__ == "__main__":
    # Test the scraper
    articles = scrape_blockchain_news()
    print(f"\nTotal articles scraped: {len(articles)}")
