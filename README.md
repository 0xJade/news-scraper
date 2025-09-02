# 🚀 Web3 News Scraper & AI Proposal Generator

A automated pipeline that scrapes blockchain news from RSS feeds, generates AI-powered research proposals using Claude AI, creates professional PDF reports, and sends email notifications. Perfect for researchers, analysts, and anyone needing to stay updated on Web3 developments with actionable insights.

## ✨ What This Project Does

### 🔍 **News Scraping**
- Automatically scrapes RSS feeds from major blockchain platforms (Ethereum, Arbitrum, Polygon, Solana, Flow)
- Filters for upgrade-related content (protocol updates, network upgrades, testnets, mainnets)
- Handles multiple RSS sources with robust error handling and logging

### 🤖 **AI-Powered Analysis**
- Integrates with Claude AI (Anthropic) to generate comprehensive research proposals
- Transforms raw news articles into structured research initiatives
- Creates detailed proposals with executive summaries, objectives, methodology, and deliverables

### 📄 **PDF Generation**
- Generates beautifully formatted PDF reports with proper markdown parsing
- Supports complex content structures (headers, lists, quotes, code blocks)
- Applies professional styling with color-coded sections and visual hierarchy
- Includes table of contents for long proposals

### 📧 **Automated Email Notifications**
- Sends PDF reports via email with secure SMTP authentication
- Supports multiple recipients, CC, BCC, and file attachments
- Comprehensive error handling and connection testing

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   RSS Scraper   │───▶│  Claude AI API   │───▶│  PDF Generator  │───▶│  Email Sender   │
│                 │    │                  │    │                 │    │                 │
│ • Ethereum      │    │ • Research       │    │ • Markdown      │    │ • SMTP          │
│ • Arbitrum      │    │   Proposals      │    │   Parsing       │    │ • Attachments   │
│ • Polygon       │    │ • Content        │    │ • Professional  │    │ • Error         │
│ • Solana        │    │   Analysis       │    │   Styling       │    │   Handling      │
│ • Flow          │    │                  │    │ • TOC           │    │                 │
└─────────────────┘    └──────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🚀 Quick Start

### 1. **Clone & Setup**
```bash
git clone <your-repo-url>
cd news_scraper
python3 -m venv news_scraper_env
source news_scraper_env/bin/activate  # On Windows: news_scraper_env\Scripts\activate
pip install -r requirements.txt
```

### 2. **Create Environment File**
Create a `.env` file in the project root:

```bash
# Anthropic API Configuration
ANTHROPIC_API_KEY=your_claude_api_key_here
ANTHROPIC_MODEL=claude-3-5-sonnet-20241022

# Email Configuration
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USER=your_email@gmail.com
EMAIL_PASSWORD=your_app_password_here
EMAIL_USE_TLS=true
```

### 3. **Get Your API Keys**

#### **Anthropic API Key**
1. Go to [Anthropic Console](https://console.anthropic.com/)
2. Sign up/Login and create an API key
3. Copy the key to your `.env` file

#### **Gmail App Password** (if using Gmail)
1. Enable 2-Step Verification on your Google Account
2. Go to [Google Account Security](https://myaccount.google.com/security)
3. Generate an "App Password" for "Mail"
4. Use this password in `EMAIL_PASSWORD` (not your regular Gmail password)

### 4. **Run the Pipeline**
```bash
python3 news_scraper_etl.py
```

## 📁 Project Structure

```
news_scraper/
├── .env                          # Environment variables (create this)
├── README.md                     # This file
├── requirements.txt              # Python dependencies
├── news_scraper_etl.py          # Main ETL pipeline
├── blockchain_news_scraper.py   # RSS scraping module
├── pdf_generator.py             # PDF report generation
├── email_sender.py              # Email notification system
└── news_scraper_env/            # Virtual environment
```

## 🔧 Configuration Details

### **Environment Variables Explained**

| Variable | Purpose | Example Value | Required |
|----------|---------|---------------|----------|
| `ANTHROPIC_API_KEY` | Your Claude AI API key for generating proposals | `sk-ant-...` | ✅ Yes |
| `ANTHROPIC_MODEL` | Claude model to use | `claude-3-5-sonnet-20241022` | ✅ Yes |
| `EMAIL_HOST` | SMTP server address | `smtp.gmail.com` | ✅ Yes |
| `EMAIL_PORT` | SMTP server port | `587` (TLS) or `465` (SSL) | ✅ Yes |
| `EMAIL_USER` | Your email address | `your_email@gmail.com` | ✅ Yes |
| `EMAIL_PASSWORD` | Your email password or app password | `your_password` | ✅ Yes |
| `EMAIL_USE_TLS` | Whether to use TLS encryption | `true` or `false` | ❌ No (defaults to `true`) |

### **Supported Email Providers**

| Provider | EMAIL_HOST | EMAIL_PORT | EMAIL_USE_TLS |
|----------|------------|------------|---------------|
| Gmail | `smtp.gmail.com` | `587` | `true` |
| Outlook | `smtp-mail.outlook.com` | `587` | `true` |
| Yahoo | `smtp.mail.yahoo.com` | `587` | `true` |
| Custom SMTP | Your server | Your port | Your choice |

## 📊 What You Get

### **Sample Output Structure**

```
📰 Web3 News Updates Report
🕒 Generated on December 15, 2024 at 2:30 PM

Ethereum Blog
  Protocol Update 002 - Scale Blobs
  Published: August 22, 2025
  Link: https://blog.ethereum.org/...
  
  # User Research Proposal: Improving Ethereum User Experience
  
  ## Executive Summary
  This proposal outlines a comprehensive user research initiative...
  
  ## Research Objectives
  • Primary Objective: Understand how to make Ethereum more accessible...
  • Secondary Objectives: Map current user journey...
  
  ## Methodology
  ### Phase 1: Foundation Research (4-6 weeks)
  - Stakeholder interviews with Protocol team members...
```

## 🛠️ Customization Options

### **Adding New RSS Sources**
Edit `blockchain_news_scraper.py`:

```python
def __init__(self):
    self.sources = {
        'ethereum_blog': 'https://blog.ethereum.org/feed.xml',
        'arbitrum_medium': 'https://medium.com/feed/@arbitrum',
        'your_new_source': 'https://your-source.com/rss.xml',  # Add here
    }
```

### **Modifying AI Prompts**
Edit the prompt in `news_scraper_etl.py`:

```python
message = client.messages.create(
    model=model,
    max_tokens=1000,
    messages=[
        {
            "role": "user",
            "content": f"Your custom prompt here: {summary}"  # Modify this
        }
    ]
)
```

### **Customizing PDF Styles**
Edit `pdf_generator.py` to modify colors, fonts, and layouts.

## 🧪 Testing & Debugging

### **Test Individual Components**

```bash
# Test scraper
python3 -c "from blockchain_news_scraper import BlockchainNewsScraper; scraper = BlockchainNewsScraper(); print(scraper.scrape_rss_feeds())"

# Test PDF generator
python3 -c "from pdf_generator import generate_enhanced_news_pdf; print('PDF generator imported successfully')"

# Test email sender
python3 -c "from email_sender import EmailSender; sender = EmailSender(); print(sender.get_config_summary())"
```

### **Test Email Connection**
```python
from email_sender import EmailSender
sender = EmailSender()
sender.test_connection()
```

### **Common Issues & Solutions**

| Issue | Cause | Solution |
|-------|-------|----------|
| "Authentication failed" | Using regular Gmail password | Generate App Password with 2FA enabled |
| "Connection refused" | Wrong port or host | Check EMAIL_HOST and EMAIL_PORT |
| "No articles found" | RSS feeds down or changed | Check source URLs manually |
| "PDF generation failed" | Missing dependencies | Install reportlab: `pip install reportlab` |

## 📈 Advanced Usage

### **Scheduled Execution**
Set up a cron job to run daily:

```bash
# Add to crontab (runs daily at 9 AM)
0 9 * * * cd /path/to/news_scraper && python3 news_scraper_etl.py
```

### **Custom Filtering**
Modify `is_upgrade_related()` in `blockchain_news_scraper.py` to change what content gets processed.

### **Batch Processing**
Process multiple sources or time periods by modifying the main pipeline.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Anthropic** for Claude AI API
- **ReportLab** for PDF generation
- **BeautifulSoup** for HTML parsing
- **Feedparser** for RSS processing

## 📞 Support

If you encounter issues:

1. Check the [Common Issues](#common-issues--solutions) section
2. Verify your `.env` configuration
3. Test individual components
4. Check the logs for detailed error messages

---

**Happy Scraping! 🚀📰🤖**
