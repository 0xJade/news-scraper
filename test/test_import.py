#!/usr/bin/env python3
"""
Test script to verify BlockchainNewsScraper import and functionality
"""

# Test import
try:
    from blockchain_news_scraper import BlockchainNewsScraper, scrape_blockchain_news
    print("✅ Successfully imported BlockchainNewsScraper")
except ImportError as e:
    print(f"❌ Import failed: {e}")
    exit(1)

# Test scraper instantiation
try:
    scraper = BlockchainNewsScraper()
    print("✅ Successfully created scraper instance")
    print(f"📰 Available sources: {list(scraper.get_sources().keys())}")
except Exception as e:
    print(f"❌ Scraper instantiation failed: {e}")
    exit(1)

# Test convenience function
try:
    print("\n🔄 Testing convenience function...")
    articles = scrape_blockchain_news()
    print(f"✅ Scraped {len(articles)} articles")
    
    if articles:
        print("\n📋 Sample articles:")
        for i, article in enumerate(articles[:2]):  # Show first 2 articles
            print(f"  {i+1}. {article['title']} ({article['source']})")
    
except Exception as e:
    print(f"❌ Convenience function failed: {e}")
    exit(1)

print("\n🎉 All tests passed! The BlockchainNewsScraper module is working correctly.")
print("\n📝 Usage in Jupyter notebook:")
print("from blockchain_news_scraper import BlockchainNewsScraper, scrape_blockchain_news")
print("articles = scrape_blockchain_news()")
