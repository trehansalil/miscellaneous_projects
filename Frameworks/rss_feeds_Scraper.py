import feedparser
import requests_cache
import time
from datetime import datetime

last_update = {
    "timestamp": None,
    "links": []
}


def fetch_podcast_data(url):

    # Use cached data if available
    with requests_cache.disabled():
        feed = feedparser.parse(rss_url)

    return feed

def read_podcast_list(rss_url):
    global last_update

    try:
        feed = fetch_podcast_data(rss_url)

        # Check if the feed was parsed successfully
        if feed.bozo:
            raise Exception("Failed to parse feed: ", feed.bozo_exception)

        print(f"Channel Title: {feed.feed.title}\n")
        print("List of Podcasts:")

        for entry in feed.entries:

            if last_update['timestamp'] is None:

                print(f"Title: {entry.title}")
                print(f"Link: {entry.link}\n")
                print(f"Publication Date: {time.strftime('%Y-%m-%d %H:%M:%S', entry.published_parsed)}\n")
                last_update['links'].append(entry.link)

            elif datetime.strptime(time.strftime('%Y-%m-%d %H:%M:%S', entry.published_parsed), '%Y-%m-%d %H:%M:%S')> last_update['timestamp']:
                if entry.link not in last_update['links']:
                    print(f"Title: {entry.title}")
                    print(f"Link: {entry.link}\n")
                    print(f"Publication Date: {time.strftime('%Y-%m-%d %H:%M:%S', entry.published_parsed)}\n")
                    last_update['links'].append(entry.link)
        last_update['timestamp'] = datetime.now()

    except Exception as e:
        print(f"Error fetching or parsing the feed: {e}")

if __name__ == "__main__":
  
    # Enable caching with a timeout of 3600 seconds (1 hour)
    requests_cache.install_cache('podcast_cache', expire_after=3600)    

    rss_feed_url = 'https://trends.google.co.in/trends/trendingsearches/daily/rss?geo=IN'
    REFRESH_FREQUENCY = 5
    while True:
        read_podcast_list(rss_url=rss_feed_url)
        time.sleep(REFRESH_FREQUENCY)
