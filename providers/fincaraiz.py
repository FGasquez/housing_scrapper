from bs4 import BeautifulSoup
import logging
from providers.base_provider import BaseProvider


class FincaRaiz(BaseProvider):
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
            properties = page_content.find_all('article', class_='MuiGrid-root')

            for prop in properties:
                # if data-id was already processed we exit
                if prop['data-id'] in processed_ids:
                    return
                processed_ids.append(prop['data-id'])
                # url = prop.find('a', class = 'MuiTypography-root')['href']
                url = prop.find('a', class_='MuiTypography-root')['href']
                title = prop.find('a', class_='MuiTypography-body1').get_text().strip()
                price_section = prop.find('span', class_='firstPrice')
                if price_section is not None:
                    title = title + ' ' + price_section['data-price']

                yield {
                    'title': title,
                    'url': url,
                    'internal_id': prop['data-id'],
                    'provider': self.provider_name
                }

            page += 1
            page_link = self.provider_data['base_url'] + source.replace("pagina=", f"pagina={page}")
