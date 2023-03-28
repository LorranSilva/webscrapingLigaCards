import scrapy
import re
import json
from scrapy_splash import SplashRequest


class LigamagicSpider(scrapy.Spider):
    name = 'ligamagic'
    allowed_domains = ['www.ligamagic.com.br']
    start_urls = ['https://www.ligamagic.com.br/?view=cards/home']


    def parse(self, response):
        collection_names = response.css('.edc-nm-1')
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
        for data in collection_page:
            yield {
                'name': data.css('b::text').get(),
                'acronym': data.css('.tb-ed-sigla::text').get(),
                'cards_quantity': data.css('.tb-cards-count::text').get(),
                'lowest_price': data.css('.tb-prc-low::text').get(),
                'avarege_price': data.css('.tb-prc-avg::text').get(),
                'highest_price': data.css('.tb-prc-max::text').get(),
                'cards': cards_data
            }
