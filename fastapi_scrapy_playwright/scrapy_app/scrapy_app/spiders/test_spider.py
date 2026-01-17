import scrapy

class TestSpider(scrapy.Spider):

    name = "test_spider"
    start_urls = ["https://example.com"]

    def parse(self, response):
        # Grab the page title
        title = response.css("title::text").get()
        yield {"url": response.url, "title": title}