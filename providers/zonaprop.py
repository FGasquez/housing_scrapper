#import requests
from bs4 import BeautifulSoup
import logging
from providers.base_provider import BaseProvider

class Zonaprop(BaseProvider):
    def props_in_source(self, source):
        page_link = self.provider_data['base_url'] + source
        page = 1
        processed_ids = []
        max_pages = 10

        while(page <= max_pages):
            logging.info(f"Requesting {page_link}")
            page_response = self.request(page_link)
            
            if page_response.status_code != 200:
                break
            
            page_content = BeautifulSoup(page_response.content, 'lxml')
            properties = page_content.find_all('div', class_='postings-container')[0]

            for prop in properties:
                price = prop.select_one('div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1)')
                if not price:
                    continue
                price = price.get_text().strip()

                title = prop.select_one('div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > h2:nth-child(3) > a:nth-child(1)')
                if not title:
                    continue
                href = title['href']
                title = title.get_text().strip()

                addr = prop.select_one('.postings-container > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(3) > div:nth-child(1)')
                if not addr:
                    addr = title
                else:
                    addr = addr.get_text().strip()
                data_id = prop.select_one('div:nth-child(1)')['data-id']
                
                yield self.process_data(source, {
                    'title': f"{addr} - {title}",
                    'url': href,
                    'internal_id': data_id
                })

            page += 1
            page_link = self.provider_data['base_url'] + source.replace(".html", f"-pagina-{page}.html")
    