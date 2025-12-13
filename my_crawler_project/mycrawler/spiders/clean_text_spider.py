import scrapy
import logging
import pandas as pd
import re
from scrapy import signals
from scrapy.http import HtmlResponse
from selenium import webdriver
from urllib.parse import urlparse, urljoin

class CleanTextSpider(scrapy.Spider):
    """
    A Scrapy spider that uses Selenium to visit pages and extract ONLY clean, 
    plain text content, ensuring one sentence per line in the output file.
    It also records visited links to an Excel file upon completion.
    """
    name = 'clean_text_spider'
    start_urls = ['https://thestjgroup.com/']
    
    
    visited_links = set()
    output_filename = 'thestjgroup.txt' # New output file
    
    def __init__(self, output_file=None, *args, **kwargs):
        super(CleanTextSpider, self).__init__(*args, **kwargs)
        # Use the provided argument, or fall back to the default
        if output_file:
            self.output_filename = output_file 

        self.driver = webdriver.Chrome()
        self.load_robots_txt(self.start_urls[0])

        # Clear the output file on start to ensure a fresh run
        with open(self.output_filename, 'w', encoding='utf-8') as f:
            f.write('')


    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        """Connects the spider_closed method to the Scrapy signal."""
        spider = super(CleanTextSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
        return spider

    def load_robots_txt(self, url):
        """Attempts to download and save the robots.txt file for the domain."""
        robots_url = urljoin(url, '/robots.txt')
        try:
            self.driver.get(robots_url)
            body = self.driver.page_source
            if body:
                with open('robots.txt', 'w', encoding='utf-8') as file:
                    file.write(body)
                self.log(f'robots.txt file saved from {robots_url}', level=logging.INFO)
        except Exception as e:
            self.log(f'Failed to load robots.txt file: {e}', level=logging.ERROR)

    def spider_closed(self, spider):
        """Executed when the spider finishes. Closes the driver and saves visited links."""
        self.driver.quit()
        # Save visited links to Excel file
        df = pd.DataFrame(list(self.visited_links), columns=["Visited Links"])
        df.to_excel('visited_links.xlsx', index=False)
        self.log(f'Scraping finished. Sentences saved to {self.output_filename}', level=logging.INFO)


    def parse(self, response):
        """
        Main parsing method. Uses Selenium to load the page, extracts clean text,
        splits it into sentences, saves it, and follows internal links.
        """
        self.driver.get(response.url)
        
        # Use Javascript (document.body.innerText) to get visible text, 
        # which automatically excludes HTML tags, scripts, and most non-visible elements.
        body_text = self.driver.execute_script("return document.body.innerText;")
        
        self.visited_links.add(response.url)
        self.log(f'Visited: {response.url}', level=logging.INFO)

        # --- Text Cleaning and Sentence Splitting ---
        
        # 1. Split text into sentences using common punctuation marks.
        # This regex ensures the punctuation is kept as part of the sentence.
        sentences = re.split(r'(?<=[.?!])\s+', body_text)
        
        # 2. Further cleaning and filtering
        cleaned_sentences = []
        for sentence in sentences:
            clean_s = sentence.strip()

            # Remove multiple spaces
            clean_s = re.sub(r'\s+', ' ', clean_s)

            # Filter out short, non-sentence fragments, or lines containing structural characters
            # that might indicate broken content or code.
            if clean_s and len(clean_s) > 10 and not re.search(r'\{|\[|\]|\<|\>', clean_s):
                
                # Simple check: Ensure the line ends with a sentence terminator 
                # or is long enough to be considered a coherent thought.
                if not (clean_s.endswith(('.', '?', '!')) or len(clean_s) < 100):
                    continue

                # Remove links/URLs that might have survived innerText
                clean_s = re.sub(r'http\S+|www\S+|\S+\.(com|net|org)\S*', '', clean_s, flags=re.IGNORECASE)

                # Remove hashtags
                clean_s = re.sub(r'#\w+', '', clean_s)
                
                cleaned_sentences.append(clean_s)

        # 3. Write each clean sentence to the output file
        with open(self.output_filename, 'a', encoding='utf-8') as f:
            for sentence in cleaned_sentences:
                # Store only a single sentence in a line, after that always start a new line
                f.write(sentence + '\n')
                
        # --- End Text Cleaning ---

        # Follow links using Scrapy's mechanism combined with Selenium's page content
        sel_response = HtmlResponse(url=self.driver.current_url, body=self.driver.page_source, encoding='utf-8')
        
        for next_page in sel_response.xpath('//a/@href').getall():
            if next_page is not None:
                next_page = response.urljoin(next_page)
                # Check if link is within the original domain and hasn't been visited
                if self.is_within_domain(next_page) and next_page not in self.visited_links:
                    self.visited_links.add(next_page)
                    yield scrapy.Request(next_page, callback=self.parse)

    def is_within_domain(self, url):
        """Checks if the URL belongs to the initial start domain."""
        parsed_url = urlparse(url)
        return parsed_url.netloc == urlparse(self.start_urls[0]).netloc
