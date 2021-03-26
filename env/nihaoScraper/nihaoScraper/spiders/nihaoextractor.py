import scrapy
import json

from nihaoScraper.items import NihaoscraperItem
from scrapy.loader import ItemLoader

class NihaoSpider(scrapy.Spider):
	
	name = 'nihao'
	allowed_domains = ['nihaojewelry.com']

	start_urls = ['https://www.nihaojewelry.com/es/']


	def parse(self, response):
		self.logger.info('In parse')
		# extract categories from the page
		
		cat_table = response.css('div.menu-head_child') 
		categories = cat_table.css('div.menu-row')


		# in each category but skips the very first
		for category in cat_table.css('div.menu-row')[1:]:

			#loader = ItemLoader(item = NihaoscraperItem(), selector = products)
			item = NihaoscraperItem() # store iteration data in each item
			# category link
			categoryLink = category.css('a').attrib['href']
			# save category name string pass category to item
			item['category'] = category.css('span::text').get()
			self.logger.info('checking category ' + category.css('span::text').get() )
			# lets check for subcategories
			yield response.follow(categoryLink, self.parse_category, cb_kwargs = dict(item = item))



	def parse_category(self, response, item):
		self.logger.info('In parse_category')
		#item = response.meta['item']  # retrieve item generated in previous request
		subcategories = response.css('div.list-content.j_option_list.j_category_type')

		# chech if the category has subcategories

		if not subcategories:
			
			self.logger.info(item['category'] + ' has no subcategories')
			item['subcategory'] = 'Sin subcategorías'

			self.logger.info('follow ' + response.request.url)

			subcategoryLink = response.request.url
			products = response.css('div.j_goods_item')
			# a more compact way is to run parse_product in the same link
			# but dunno how make it 
			if products:

				# search for products in the page
				for product in products:

					item['name'] = product.css('p.remark a::text').get()
					item['price'] = product.css('div.row-item span:nth-child(2)::text').get().replace('MX$ ','')
					item['link'] = product.css('p.remark a').attrib['href']

					yield response.follow(product.css('p.remark a').attrib['href'], self.parse_details, cb_kwargs = dict(item = item))

		else:

			# in each subcategory
			for subcategory in subcategories.css('a'):

				self.logger.info('from ' + item['category'] + ' checking ' + subcategory.css('a::text').get())
				item['subcategory'] = subcategory.css('a::text').get()

				subcategoryLink = subcategory.css('a').attrib['href']

				self.logger.info('follow ' + subcategoryLink)
				yield response.follow(subcategoryLink, self.parse_product, cb_kwargs = dict(item = item))



	def parse_product(self, response, item):
		self.logger.info('In parse_product')
		self.logger.info('Scraping products from ' + response.request.url)
		# save products as list
		products = response.css('div.j_goods_item')

		# if list is not null
		# acctualy it can be tweaked to just crawl pages with x products
		if products:

			# search for products in the page
			for product in products:

				item['name'] = product.css('p.remark a::text').get()
				item['price'] = product.css('div.row-item span:nth-child(2)::text').get().replace('MX$ ','')
				item['link'] = product.css('p.remark a').attrib['href']
				# here we must check for each detail product
				yield response.follow(product.css('p.remark a').attrib['href'], self.parse_details, cb_kwargs = dict(item = item))
				

			# redirect to next page if exists
			next_page = response.css('a.next').attrib['href']

			#if next_page is not None:
			#	yield response.follow(next_page, callback=self.parse_product, cb_kwargs=dict(item = item))


	def parse_details(self, response, item):
		self.logger.info('In parse_details')

		# there is a variable in the script with this pattern
		pattern = r'\bvar\s+iDetailData\s*=(\{.*?\})\s*;\s*\n'

		# transcrip the pattern to json 
		json_data = response.css('script::text').re_first(pattern)

		buy_info = response.css('div.buy-info')
		details = json.loads(json_data)

		item['currencyRate'] = details['currencyRate']
		item['priceDiscount'] = details['priceDiscount']

		# some products are arrays of the same product
		for subproduct in details['skuTieredPrices']: 

			item['specialPrice'] = subproduct['specialPrice']
			item['productPrice'] = subproduct['price']
			item['weight'] = subproduct['weight']
			item['stock'] = subproduct['inventory']

			yield item



