import re
import pandas as pd
import base64
import io
from itemadapter import ItemAdapter

class CleanTextPipeline:
    """Pipleline to clean text items, split into sentences, filter unwanted fragments(non-sentences), and save results.
       Also handles saving visited links at the end of the crawl.
       Encode the text and excel file to a base64 string
    """
    def __init__(self):
        self.sentences = []
        self.visited_links = set()
        self.robots_txt_content = None

    def process_item(self, item, spider):
        adapter=ItemAdapter(item) 
        
        # Handle robots.txt content
        robots_txt = adapter.get('robots_txt')
        if robots_txt:
            self.robots_txt_content = robots_txt
            return item

        #Handle other text items
        text = adapter.get('text', '')
        url=adapter.get('url', '')
        if url:
            self.visited_links.add(url)

        #Split and clean sentences
        sentences=re.split(r'[?<=[.?!]]\s+', text)
        for sentence in sentences:
            clean_s=sentence.strip()
            clean_s=re.sub(r'\s+', ' ', clean_s)

            if clean_s and len(clean_s)>10 and not re.search(r'\{|\[|\]|\<|\>}', clean_s):
                if not(clean_s.endswith('.','?','!')) or len(clean_s)<100:
                    continue
                
                clean_s=re.sub(r'http\S+|www\S+|https\S+\.(com|net|org)', '', clean_s, flags=re.IGNORECASE)
                clean_s=re.sub(r'#\w+', '', clean_s)
                self.sentences.append(clean_s)

        return item
    
    def close_spider(self, spider):
        # --- Encode sentences into Base64 text file ---
        text_content = "\n".join(self.sentences)
        text_b64 = base64.b64encode(text_content.encode("utf-8")).decode("utf-8")

        df = pd.DataFrame(list(self.visited_links), columns=['Visited Links'])
        excel_bytes = io.BytesIO()

        df.to_excel(excel_bytes, index=False, engine="openpyxl")
        excel_b64 = base64.b64encode(excel_bytes.getvalue()).decode("utf-8")

        # --- Encode robots.txt into Base64 ---
        robots_b64 = None
        if self.robots_txt_content:
            robots_b64 = base64.b64encode(self.robots_txt_content.encode("utf-8")).decode("utf-8")

        #Instead of writing files, yield the final encoded results
        spider.crawler.stats.set_value("text_file_base64", text_b64)
        spider.crawler.stats.set_value("excel_file_b64", excel_b64)
        if robots_b64:
            spider.crawler.stats.set_value("robots_txt_base64", robots_b64)

        spider.log(
            "Pipeline finished. Base 64 files encoded and attached to Zyte job output.",
            level="INFO"
        )