import scrapy
import re
import json
from scrapy_splash import SplashRequest


class LigaygoSpider(scrapy.Spider):
    name = 'ligaygo'
    allowed_domains = ['www.ligayugioh.com.br']
    start_urls = ['https://www.ligayugioh.com.br/?view=cards/home']

    def parse(self, response):
        collection_names = response.css('.edc-nm-3')
        for name in collection_names:
            next_page = {}
            next_page['link'] = name.xpath('a/@href').extract()
            if next_page['link'] is not None:
                for link in next_page['link']:
                    url = response.follow(link)
                    yield SplashRequest(url.url, callback=self.parse_splash, args={'wait': 0.7})

    def parse_splash(self, response):
        script_text = response.xpath("//script[contains(., 'var cardsjson =')]/text()").get()
        json_string = re.search(r"var cardsjson = (\[.*?\]);", script_text).group(1)
        cards_data = json.loads(json_string)
        collection_page = response.css('.tb-ed')
        lowest_price = sum(map(lambda x: float(x['precoMenor']), cards_data))
        highest_price = sum(map(lambda x: float(x['precoMaior']), cards_data))
        medium_price = (lowest_price + highest_price)/2
        for data in collection_page:
            yield {
                'name': data.css('b::text').get(),
                'acronym': data.css('.tb-ed-sigla::text').get(),
                'cards_quantity': len(cards_data),
                'lowest_price': float(f"{lowest_price:.2f}"),
                'averege_price': float(f"{medium_price:.2f}"),
                'highest_price': float(f"{highest_price:.2f}"),
                'cards': cards_data
            }