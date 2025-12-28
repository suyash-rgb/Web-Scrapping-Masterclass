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
        yield SplashRequest(url=self.start_url, callback=self.parse, args={'wait': 1})

    def parse(self, response):
        text_nodes = response.css("body *::text").getall()
        sentences = [s.strip() for s in text_nodes if s.strip()]
        for sentence in sentences:
            yield {"sentence": sentence, "url": response.url}

        for link in response.css("a::attr(href)").getall():
            abs_url = response.urljoin(link)
            if self.is_within_domain(abs_url) and abs_url not in self.visited_links:
                self.visited_links.add(abs_url)
                yield SplashRequest(url=abs_url, callback=self.parse, args={'wait': 1})

    def is_within_domain(self, url):
        return urlparse(url).netloc == urlparse(self.start_url).netloc