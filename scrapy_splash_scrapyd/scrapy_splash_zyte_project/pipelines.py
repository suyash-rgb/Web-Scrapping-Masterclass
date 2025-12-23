
import re
import pandas as pd
from itemadapter import ItemAdapter

class CleanTextPipeline:
    """Pipleline to clean text items, split into sentences, filter unwanted fragments(non-sentences), and save results.
       Also handles saving visited links at the end of the crawl.
    """
    def __init__(self):
        self.sentences = []
        self.visited_links = set()

    def process_item(self, item, spider):
        adapter=ItemAdapter(item)
        text = adapter.get('text', '')
        url=adapter.get('url', '')
        if url:
            self.visited_links.add(url)

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
        """Called when the spider finishes. Save cleaned sentences and visited links."""
        output_file=getattr(spider, "ouput_filename", "output.txt")
        with open(output_file, 'w', encoding='utf-8') as f:
            for sentence in self.sentences:
                f.write(sentence + '\n')

        df=pd.DataFrame(list(self.visited_links), columns=['Visited Links'])
        df.to_excel('visited_links.xlsx', index=False)

        spider.log(f"Pipeline finished. Sentences saved to {output_file}", level="INFO")