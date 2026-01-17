import scrapy

class QuotesSpider(scrapy.Spider):
    name = "quotes_spider"
    start_urls = ["https://quotes.toscrape.com/js/"]

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(
                url,
                meta={"playwright": True},  # enable JS rendering
                callback=self.parse,
            )

    def parse(self, response):
        for quote in response.css("div.quote"):
            yield {
                "text": quote.css("span.text::text").get(),
                "author": quote.css("small.author::text").get(),
                "tags": quote.css("div.tags a.tag::text").getall(),
            }

        # follow pagination
        next_page = response.css("li.next a::attr(href)").get()
        if next_page:
            yield scrapy.Request(
                response.urljoin(next_page),
                meta={"playwright": True},
                callback=self.parse,
            )