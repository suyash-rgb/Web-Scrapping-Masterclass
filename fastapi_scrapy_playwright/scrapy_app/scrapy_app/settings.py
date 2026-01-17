BOT_NAME = "scrapy_app"

SPIDER_MODULES = ["scrapy_app.spiders"]
NEWSPIDER_MODULE = "scrapy_app.spiders"

# Enable Playwright for JS rendering
DOWNLOAD_HANDLERS = {
    "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
    "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
}

# Use asyncio reactor (required for scrapy-playwright)
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"

# Playwright browser settings
PLAYWRIGHT_BROWSER_TYPE = "chromium"
PLAYWRIGHT_LAUNCH_OPTIONS = {"headless": True}
# Avoid noisy shutdown errors on Windows
PLAYWRIGHT_PROCESS_REQUEST_HEADERS = None

# Crawl responsibly
ROBOTSTXT_OBEY = True

# Concurrency & performance tuning (safe defaults for small sites)
CONCURRENT_REQUESTS = 2
DOWNLOAD_DELAY = 0.25  # small delay between requests
PLAYWRIGHT_DEFAULT_NAVIGATION_TIMEOUT = 30_000  # 30 seconds

# Logging
LOG_LEVEL = "INFO"

# Output encoding
FEED_EXPORT_ENCODING = "utf-8"

# Prevent noisy shutdown errors from Playwright on Windows
EXTENSIONS = {
    'scrapy.extensions.corestats.CoreStats': 500,
    'scrapy.extensions.logstats.LogStats': 500,
    'scrapy.extensions.telnet.TelnetConsole': None,  # disable telnet
}