import scrapy
import scrapy_splash
from scrapy_splash import SplashRequest

class CleanTextSpider(scrapy.Spider):
    name = "clean_text_spider"
    start_urls=['https://thestjgroup.com/']

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse, args={'wait': 2}) #splash request instead of request to render JS
        
    def parse(self, response):
        
        #yield items
        yield{
            "url": response.url,
            "text": response.text #raw rendered HTML or text
        }

        #follow internal links
        for next_page in response.css('a::attr(href)').getall():
            next_page=response.urljoin(next_page)
            if self.is_within_domain(next_page):
                yield SplashRequest(next_page, self.parse, args={'wait': 2})

    def is_within_domain(self, url):
        return url.startswith(self.start_urls[0])
