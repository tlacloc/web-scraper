import pandas as pd
import scrapy

class productsExtractorSpider(scrapy.Spider):
	name = 'productsSpider'

	# page to scrap
	targets = pd.read_json('subcategories.json')
	start_urls = targets["link"].values.tolist()


	def parse(self, response):
		for product in response.css('div.j_goods_item'):
			yield {
				'name': product.css('p.remark a::text').get()  ,
				'price': product.css('div.row-item span:nth-child(2)::text').get().replace('MX$ ',''),
				'link': product.css('p.remark a').attrib['href'],
			}
		# buscando más páginas para scrap
		next_page = response.css('a.next').attrib['href']
		if next_page is not None:
			yield response.follow(next_page, callback=self.parse)