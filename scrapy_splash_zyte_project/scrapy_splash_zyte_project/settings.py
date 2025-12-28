
BOT_NAME = "scrapy_splash_zyte_project"

SPIDER_MODULES = ["scrapy_splash_zyte_project.spiders"]
NEWSPIDER_MODULE = "scrapy_splash_zyte_project.spiders"

ADDONS = {}

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

SPLASH_URL = "http://splash:8050"

DOWNLOADER_MIDDLEWARES = {
    'scrapy_splash.SplashCookiesMiddleware': 723,
    'scrapy_splash.SplashMiddleware': 725,
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
}

SPIDER_MIDDLEWARES = {
    'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
}

DUPEFILTER_CLASS = 'scrapy_splash.SplashAwareDupeFilter'
HTTPCACHE_STORAGE = 'scrapy_splash.SplashAwareFSCacheStorage'

# Concurrency and throttling settings
#CONCURRENT_REQUESTS = 16
CONCURRENT_REQUESTS_PER_DOMAIN = 1
DOWNLOAD_DELAY = 1

FEED_EXPORT_ENCODING = "utf-8"
