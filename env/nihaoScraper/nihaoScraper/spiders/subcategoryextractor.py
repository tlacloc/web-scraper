import scrapy
import pandas as pd


# update: 23 may 2021

class subcategoryExtractorSpider(scrapy.Spider):
	name = 'subcategorySpider'
	
	# page to scrap

	targets = pd.read_json('categories.json')
	start_urls = targets["link"].values.tolist()

	def parse(self, response):

		#
		targets = pd.read_json('categories.json')
		subcategories = response.css('div.list-content.j_option_list.j_category_type')
		for subcategory in subcategories.css('a'):
		    yield {
			#'category' : targets[targets['link'] == response.request.url]['category'],
			'subcategory': subcategory.css('a::text').get(),
			'link': subcategory.css('a').attrib['href']
 			}

 		#if not subcategories:
 		#    yield {
			#'category' : targets[targets['link'] == response.request.url]['category'],
		#	'subcategory': 'sin subcategorias',
		#	'link': response.request.url
 		#	}