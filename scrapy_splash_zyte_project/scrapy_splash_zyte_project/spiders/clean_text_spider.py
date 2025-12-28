import scrapy
from scrapy_splash import SplashRequest
from urllib.parse import urlparse

class CleanTextSplashSpider(scrapy.Spider):
    name = "clean_text_splash_spider"

    def __init__(self, start_url=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not start_url:
            raise ValueError("You must provide a start_url using -a start_url=<URL>")
        self.start_url = start_url
        self.visited_links = set()

    def start_requests(self):
        # Request robots.txt file first
        domain = urlparse(self.start_url).scheme + "://" + urlparse(self.start_url).netloc
        robots_url = domain + "/robots.txt"
        yield scrapy.Request(url=robots_url, callback=self.parse_robots, dont_filter=True)

        # the start crawling with Splash
        yield SplashRequest(url=self.start_url, callback=self.parse, args={'wait': 1})

    def parse_robots(self, response):
        # Yield the robots.txt content for pipeling
        yield {
            "robots_txt": response.text,
            "url": response.url
        }

    def parse(self, response):
        #first collect raw text from the page
        body_text = " ".join(response.css("body *::text").getall())
        yield {
            "text": body_text,
            "url": response.url
        }

        #Follow links within the same domain
        for link in response.css("a::attr(href)").getall():
            abs_url = response.urljoin(link)
            if self.is_within_domain(abs_url) and abs_url not in self.visited_links:
                self.visited_links.add(abs_url)
                yield SplashRequest(url=abs_url, callback=self.parse, args={'wait': 1})

    def is_within_domain(self, url):
        return urlparse(url).netloc == urlparse(self.start_url).netloc