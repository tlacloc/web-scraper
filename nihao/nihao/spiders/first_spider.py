import scrapy


class NihaoSpider(scrapy.Spider):
    name = "first_spider"
    start_urls = [
        'https://www.nihaojewelry.com/retro-small-round-buckle-fine-belt-female-gun-black-buckle-hollow-eye-ladies-belt-fashion-puffy-belt-women-nhpo198250.html']

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = f'belt-{page}.html'
        with open(filename, 'wb') as f:
            f.write(response.body)