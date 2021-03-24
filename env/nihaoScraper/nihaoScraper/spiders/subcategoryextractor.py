import scrapy
import pandas as pd


# update: 23 may 2021
#
#
#
# search for sub categories in the page
# return a json file with
# subcategories = {
#			'category' = category name
#			'subcategory' = subcategory name
#			'url = subcategory url'
# }
#
#


class subcategoryExtractorSpider(scrapy.Spider):
	name = 'subcategorySpider'
	
	# page to scrap

	targets = pd.read_json('categories.json')
	start_urls = targets["link"].values.tolist()

	def parse(self, response):

		#
		subcategories = response.css('div.list-content.j_option_list.j_category_type')
		for subcategory in subcategories.css('a'):
			yield {
#			'category' = category name
			'subcategory': subcategory.css('a::text').get(),
			'link': subcategory.css('a').attrib['href']
 			}