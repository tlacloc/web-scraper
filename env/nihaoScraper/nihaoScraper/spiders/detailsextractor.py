import scrapy
import chompjs


class productsExtractorSpider(scrapy.Spider):

	name = 'detailsSpider'

	# page to scrap
	targets = pd.read_json('products.json')

	# urls from file
	start_urls = targets["link"].values.tolist()

	def parse(self, response):

		# javascript to json dic
		javascript = response.css('script::text').get()
		data = chompjs.parse_js_object(javascript)
		details = response.css('script')[-12].get()   
