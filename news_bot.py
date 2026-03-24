import feedparser
import os
from datetime import datetime

RSS_FEEDS = {
    "Reuters Business": "https://feeds.reuters.com/reuters/businessNews",
    "Reuters Markets":  "https://feeds.reuters.com/reuters/marketsNews",
    "Yahoo Finance":    "https://finance.yahoo.com/news/rssindex",
    "MarketWatch":      "https://feeds.marketwatch.com/marketwatch/marketpulse/",
    "CNBC Markets":     "https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=20910258",
}

KEYWORDS = [
    "nasdaq", "s&p 500", "dow jones", "fed", "federal reserve",
    "interest rate", "inflation", "trump", "iran", "china", "tariff",
    "nvidia", "apple", "microsoft", "tech stock", "market crash",
    "oil", "crude", "recession", "gdp", "jobs report",
    "rate cut", "rate hike", "powell", "bond yield", "war",
    "geopolitical", "earnings", "ceasefire", "sanctions"
]

def fetch_all_news():
    all_news = []
    for source, url in RSS_FEEDS.items():
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:15]:
                title = entry.get('title', '')
                summary = entry.get('summary', '')
                published = entry.get('published', '')
                combined = (title + summary).lower()
                if any(kw in combined for kw in KEYWORDS):
                    all_news.append({
                        'source': source,
                        'title': title,
                        'summary': summary[:400],
                        'published': published
                    })
        except Exception as e:
            print(f"Lỗi {source}: {e}")
    return all_news

def create_mirofish_file(news_list):
    now = datetime.now().strftime("%Y-%m-%d %H:%M UTC")
    filename = f"nasdaq_auto_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"

    content = f"""TRADING NEWS AUTO-FEED - {now}
Sources: Reuters, CNBC, Yahoo Finance, MarketWatch
Total articles found: {len(news_list)}
{'='*60}

"""
    for news in news_list:
        content += f"""
SOURCE: {news['source']}
TIME: {news['published']}
HEADLINE: {news['title']}
SUMMARY: {news['summary']}
{'─'*50}
"""

    # Lưu vào folder output
    os.makedirs('output', exist_ok=True)
    filepath = f"output/{filename}"
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"✅ Đã tạo: {filepath} ({len(news_list)} tin)")
    return filepath

if __name__ == "__main__":
    print(f"🤖 Đang cào tin lúc {datetime.now().strftime('%H:%M:%S')}...")
    news = fetch_all_news()
    if news:
        create_mirofish_file(news)
    else:
        print("⚠️ Không tìm thấy tin liên quan")