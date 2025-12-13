# Scrapy settings for mycrawler project

BOT_NAME = 'mycrawler'
SPIDER_MODULES = ['mycrawler.spiders']
NEWSPIDER_MODULE = 'mycrawler.spiders'

# Obey robots.txt rules (set to False since your spider handles its own robots.txt download,
# but Scrapy should typically honor it for good practice).
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 4

# Configure a delay for requests for the same website (default: 0)
# This is a crucial setting when using Selenium/Webdriver to avoid overwhelming the site.
DOWNLOAD_DELAY = 3

# Disable Telnet Console (enabled by default)
TELNETCONSOLE_ENABLED = False

# Disable cookies (optional, but often helps with cleaning)
COOKIES_ENABLED = False

# Configure item pipelines (optional, not strictly needed for direct file output)
# ITEM_PIPELINES = {
#    'mycrawler.pipelines.MycrawlerPipeline': 300,
# }

# Set the maximum depth that Scrapy will crawl (if not specified in the spider)
# DEPTH_LIMIT = 5 
