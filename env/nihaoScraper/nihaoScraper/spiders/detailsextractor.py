import scrapy
import json
import pandas as pd
#import chompjs
# for some reason the env doents loads chompjs

class detailsExtractorSpider(scrapy.Spider):

	name = 'detailsSpider'

	# page to scrap
	targets = pd.read_json('products.json')

	# urls from file
	#start_urls = targets["link"].values.tolist()
	start_urls = ['https://www.nihaojewelry.com/es/conjunto-de-pulsera-cuernos-luna-con-diamantes-nhgy326659.html']

	def parse(self, response):

		# javascript to json dic
		#javascript = response.css('script::text').get()
		#data = chompjs.parse_js_object(javascript)
		#details = response.css('script')[-12].get()   

		# json script to json dic by json library
		# pattern of the variable
		pattern = r'\bvar\s+iDetailData\s*=(\{.*?\})\s*;\s*\n'
		json_data = response.css('script::text').re_first(pattern)

		# extract more data from buy-info
		# just to make more easy to work it later
		buy_info = response.css('div.buy-info')


		yield { 
			'item id': buy_info.css('div.remark span::text').get().replace('Item No.: ',''),
			'product name': response.css('title::text').get(),
			'data': json.loads(json_data)
			}
