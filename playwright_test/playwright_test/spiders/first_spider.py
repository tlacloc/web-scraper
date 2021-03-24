import scrapy
import playwright

class AwesomeSpiderWithPage(scrapy.Spider):
    name = "page"

    def start_requests(self):
        yield scrapy.Request(
            url="https://www.nihaojewelry.com/the-latest-updates/03-20-2021",
            meta={"playwright": True, "playwright_include_page": True},
        )

    async def parse(self, response):
        page = response.meta["playwright_page"]
        title = await page.title()  # "Example Domain"
        yield {"title": title}
        await page.close()
        filename = f'page-{page}.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log(f'Saved file {filename}')