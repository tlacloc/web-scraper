import scrapy

# update: 23 may 2021
#
#
#
# search for categories in the page
# return a json file with
# categories = {
#			'category' = category name
#			'url = category url'
# }
#
#

class categoryExtractorSpider(scrapy.Spider):
	name = 'categorySpider'

	# page to scrap
	start_urls = ['https://www.nihaojewelry.com/es/']


	def parse(self, response):

		# this is for searching div.menu-row in div.menu-head_child
		cat_table = response.css('div.menu-head_child')
		categories = cat_table.css('div.menu-row')

		# in each category
		# but skips the very first one
		for category in categories[1:]: 

			# for print as json
			yield {
				'category': category.css('span::text').get()  ,
				'link': category.css('a').attrib['href']
			}

