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
		cat_table = response.css('div.menu-head_child') # extract categories from the page
		# in each category but skips the very first
		for index, category in enumerate(cat_table.css('div.menu-row')[1:]):
			if index != 10 and index != 8 and index != 5 and index != 4: # remove some categories
				item = NihaoscraperItem() # store iteration data in each item
				categoryLink = category.css('a').attrib['href']  + '?order=price&dir=ASC' # category link
				item['category'] = category.css('span::text').get() # save category name string pass category to item
				self.logger.info('checking category ' + category.css('span::text').get())			
				# lets check for subcategories
				yield scrapy.Request(categoryLink, self.parse_category, cb_kwargs = dict(item = item))


	def parse_category(self, response, item):
		self.logger.info('In parse_category')
		#item = response.meta['item']  # retrieve item generated in previous request
		subcategories = response.css('div.list-content.j_option_list.j_category_type')

		if not subcategories: # chech if the category has subcategories
			self.logger.info(item['category'] + ' has no subcategories')
			self.logger.info('follow ' + response.request.url)

			item['subcategory'] = 'Sin subcategorías'
			subcategoryLink = response.request.url
			products = response.css('div.j_goods_item')
			# a more compact way is to run parse_product in the same link
			# but dunno how do it 
			if products:
				# search for products in the page
				for product in products:
					item['name'] = product.css('p.remark a::text').get()
					item['link'] = product.css('p.remark a').attrib['href']
					try: # save data as float value
						item['price'] = float(product.css('div.row-item span:nth-child(2)::text').get().replace('MX$ ',''))
					except:
						self.logger.info('invalid value for price')

					yield scrapy.Request(product.css('p.remark a').attrib['href'], 
						self.parse_details, cb_kwargs = dict(item = item))

			current_page_number = response.css('a.is-current::text').get() # pdw web
			if int(current_page_number) < 10: # check only the first 10 pages
				next_page = response.css('a.next').attrib['href']
				if next_page is not None: # redirect to next page if exists
					yield scrapy.Request(next_page, callback=self.parse_product, cb_kwargs=dict(item = item))
				
		else:
			for subcategory in subcategories.css('a'): # in each subcategory
				self.logger.info('from ' + item['category'] + ' checking ' + subcategory.css('a::text').get())
				item['subcategory'] = subcategory.css('a::text').get()
				# subcategory link ordered by price
				subcategoryLink = subcategory.css('a').attrib['href']  + '?order=price&dir=ASC' 
				self.logger.info('follow ' + subcategoryLink)
				yield scrapy.Request(subcategoryLink, self.parse_product, cb_kwargs = dict(item = item))


	def parse_product(self, response, item):
		self.logger.info('In parse_product')
		self.logger.info('Scraping products from ' + response.request.url)
		products = response.css('div.j_goods_item') # save products as list
		# if list is not null
		# acctualy it can be tweaked to just crawl pages with x products
		if products:
			# search for products in the page
			for product in products:
				item['name'] = product.css('p.remark a::text').get()
				item['link'] = product.css('p.remark a').attrib['href']
				try: # try save price as float value
					item['price'] = float(product.css('div.row-item span:nth-child(2)::text').get().replace('MX$ ',''))
				except: #
					self.logger.info('invalid value for price')
				# here we must check for each detail product
				yield scrapy.Request(product.css('p.remark a').attrib['href'], 
					self.parse_details, cb_kwargs = dict(item = item))
			current_page_number = response.css('a.is-current::text').get() # pdw page
			if int(current_page_number) < 10: #check just the first 10 pages
				next_page = response.css('a.next').attrib['href']
				if next_page is not None: # redirect to next page if exists
					yield scrapy.Request(next_page, callback=self.parse_product, cb_kwargs=dict(item = item))


	def parse_details(self, response, item):
		self.logger.info('In parse_details')
		pattern = r'\bvar\s+iDetailData\s*=(\{.*?\})\s*;\s*\n' # there is a variable in the script with this pattern
		json_data = response.css('script::text').re_first(pattern) # transcrip the pattern to json 
		buy_info = response.css('div.buy-info')
		item['product_key'] = buy_info.css('div.remark span::text').get().replace('Item No.: ','') # save product ID
		details = json.loads(json_data) # details json var
		
		for subproduct in details['skuTieredPrices']: # some products are arrays of the same product
			item['subProductName'] = subproduct['sku']
			item['weight'] = subproduct['weight']
			item['stock'] = subproduct['inventory']
			item['subProductPrice'] = details['currencyRate'] * subproduct['price']
			yield item



