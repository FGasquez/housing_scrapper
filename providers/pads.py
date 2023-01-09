from bs4 import BeautifulSoup
import logging
from providers.base_provider import BaseProvider
import re


class Pads(BaseProvider):
    def props_in_source(self, source):
        page_link = self.provider_data['base_url'] + source
        page = 1
        processed_ids = []

        while True:
            logging.info(f"Requesting {page_link}")
            page_response = self.request(page_link)

            if page_response.status_code != 200:
                break

            page_content = BeautifulSoup(page_response.content, 'lxml')
            properties = page_content.find_all('ul', class_=re.compile('SearchViewstyled__ListSearch.*'))

            for prop in properties[0].children:
                url = prop.find('a', class_=re.compile('ProductCardDetailstyle__CardContentContainer.*'))['href']
                internal_id = re.search(r'(https://)?(www\.)?(pads\.com\.co\/)?(\d+)', url).group(4)

                if internal_id in processed_ids:
                    return
                processed_ids.append(internal_id)
                title = prop.find('div',
                                  class_=re.compile('ProductCardDetailstyle__NeighborhoodContent.*')).get_text().strip()
                price_section = prop.find('div', class_=re.compile('ProductCardDetailstyle__PriceContent.*'))
                if price_section is not None:
                    title = title + ' ' + price_section.get_text()

                yield {
                    'title': title,
                    'url': url,
                    'internal_id': internal_id,
                    'provider': self.provider_name
                }

            page += 1
            page_link = self.provider_data['base_url'] + source.replace("pagina=", f"pagina={page}")
