import feedparser
import requests
import os
from datetime import datetime

# ═══════════════════════════════════════════════
# NGUỒN TIN MỞ RỘNG - TẤT CẢ FREE
# ═══════════════════════════════════════════════
RSS_FEEDS = {
    # === BREAKING NEWS ===
    "Reuters Breaking":     "https://feeds.reuters.com/reuters/breakingviews",
    "Reuters Business":     "https://feeds.reuters.com/reuters/businessNews",
    "Reuters Markets":      "https://feeds.reuters.com/reuters/marketsNews",
    
    # === US MARKETS ===
    "CNBC Markets":         "https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=20910258",
    "CNBC Finance":         "https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=10000664",
    "MarketWatch":          "https://feeds.marketwatch.com/marketwatch/marketpulse/",
    "Yahoo Finance":        "https://finance.yahoo.com/news/rssindex",
    "Seeking Alpha":        "https://seekingalpha.com/market_currents.xml",
    
    # === FINANCIAL BREAKING ===
    "Investing.com":        "https://www.investing.com/rss/news_25.rss",
    "Benzinga":             "https://www.benzinga.com/feed",
    "FXStreet":             "https://www.fxstreet.com/rss/news",
    "ForexLive":            "https://www.forexlive.com/feed/news",
    
    # === GOOGLE NEWS (BREAKING) ===
    "Google News Finance":  "https://news.google.com/rss/search?q=stock+market+nasdaq&hl=en-US&gl=US&ceid=US:en",
    "Google News Fed":      "https://news.google.com/rss/search?q=federal+reserve+interest+rate&hl=en-US&gl=US&ceid=US:en",
    "Google News Geopo":    "https://news.google.com/rss/search?q=iran+israel+war+oil+market&hl=en-US&gl=US&ceid=US:en",
    "Google News Trump":    "https://news.google.com/rss/search?q=trump+economy+tariff+market&hl=en-US&gl=US&ceid=US:en",
    
    # === CRYPTO (ảnh hưởng risk sentiment) ===
    "CoinDesk":             "https://www.coindesk.com/arc/outboundfeeds/rss/",
    "CoinTelegraph":        "https://cointelegraph.com/rss",
}

# Từ khoá lọc
KEYWORDS = [
    # Markets
    "nasdaq", "s&p 500", "s&p500", "dow jones", "russell 2000",
    "stock market", "wall street", "equity", "bull", "bear",
    # Fed & Macro  
    "federal reserve", "fed", "fomc", "interest rate", "rate cut",
    "rate hike", "powell", "inflation", "cpi", "ppi", "gdp",
    "recession", "stagflation", "treasury", "bond yield",
    # Geopolitical BREAKING
    "trump", "iran", "israel", "russia", "ukraine", "china",
    "tariff", "sanction", "ceasefire", "war", "strike", "attack",
    "oil", "crude", "opec", "energy", "lng", "pipeline",
    "strait of hormuz", "middle east",
    # Tech stocks
    "nvidia", "apple", "microsoft", "amazon", "google", "meta",
    "tesla", "smci", "ai chip", "semiconductor",
    # Signals
    "market crash", "circuit breaker", "halt", "plunge", "surge",
    "record high", "record low", "all time high", "correction",
    "earnings", "guidance", "revenue beat", "revenue miss",
]

# Từ khoá BREAKING NEWS ưu tiên cao
BREAKING_KEYWORDS = [
    "breaking", "urgent", "alert", "just in", "developing",
    "ceasefire", "war declared", "emergency", "crisis",
    "market halt", "circuit breaker", "fed emergency",
    "rate cut surprise", "rate hike surprise",
]

def fetch_all_news():
    all_news = []
    breaking_news = []
    
    for source, url in RSS_FEEDS.items():
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:20]:
                title = entry.get('title', '')
                summary = entry.get('summary', '')
                published = entry.get('published', '')
                link = entry.get('link', '')
                combined = (title + summary).lower()
                
                # Check breaking news
                is_breaking = any(kw in combined for kw in BREAKING_KEYWORDS)
                
                # Check relevant keywords
                if any(kw in combined for kw in KEYWORDS):
                    news_item = {
                        'source': source,
                        'title': title,
                        'summary': summary[:500],
                        'published': published,
                        'link': link,
                        'is_breaking': is_breaking
                    }
                    if is_breaking:
                        breaking_news.append(news_item)
                    else:
                        all_news.append(news_item)
        except Exception as e:
            print(f"Lỗi {source}: {e}")
    
    return breaking_news, all_news

def create_mirofish_file(breaking_news, all_news):
    now = datetime.now().strftime("%Y-%m-%d %H:%M UTC")
    filename = f"nasdaq_auto_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
    total = len(breaking_news) + len(all_news)

    content = f"""TRADING NEWS AUTO-FEED - {now}
Sources: Reuters, CNBC, MarketWatch, Yahoo Finance, Investing.com, 
         Benzinga, FXStreet, ForexLive, Google News, CoinDesk
Total articles: {total} | Breaking: {len(breaking_news)} | Regular: {len(all_news)}
{'='*60}

"""
    # BREAKING NEWS TRƯỚC
    if breaking_news:
        content += f"""
🚨🚨🚨 BREAKING NEWS ({len(breaking_news)} articles) 🚨🚨🚨
{'='*60}
"""
        for news in breaking_news:
            content += f"""
⚡ BREAKING - {news['source']}
TIME: {news['published']}
HEADLINE: {news['title']}
SUMMARY: {news['summary']}
LINK: {news['link']}
{'─'*50}
"""

    # TIN THƯỜNG
    content += f"""

📰 MARKET NEWS ({len(all_news)} articles)
{'='*60}
"""
    for news in all_news:
        content += f"""
SOURCE: {news['source']}
TIME: {news['published']}
HEADLINE: {news['title']}
SUMMARY: {news['summary']}
{'─'*50}
"""

    os.makedirs('output', exist_ok=True)
    filepath = f"output/{filename}"
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"✅ File: {filepath}")
    print(f"🚨 Breaking news: {len(breaking_news)}")
    print(f"📰 Regular news: {len(all_news)}")
    return filepath

if __name__ == "__main__":
    print(f"🤖 Cào tin lúc {datetime.now().strftime('%H:%M:%S UTC')}...")
    breaking, regular = fetch_all_news()
    if breaking or regular:
        create_mirofish_file(breaking, regular)
    else:
        print("⚠️ Không tìm thấy tin")
