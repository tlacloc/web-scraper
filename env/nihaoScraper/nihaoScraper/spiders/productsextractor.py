import pandas as pd
import scrapy

# update 24 march 2021

class productsExtractorSpider(scrapy.Spider):

	name = 'productsSpider'

	# page to scrap
	targets = pd.read_json('subcategories.json')

	# urls from file
	start_urls = targets["link"].values.tolist()


	def parse(self, response):

		# save products as list
		products = response.css('div.j_goods_item')

		# if list is not null
		# acctualy it can be tweaked to just
		# crawl pages with x products
		if len(products) == 60:

			# search for products in the page
			for product in products:

				yield {
					'name': product.css('p.remark a::text').get()  ,
					'price': product.css('div.row-item span:nth-child(2)::text').get().replace('MX$ ',''),
					'link': product.css('p.remark a').attrib['href'],
				}

			# redirect to next page if exists
			next_page = response.css('a.next').attrib['href']
			if next_page is not None:
				yield response.follow(next_page, callback=self.parse)