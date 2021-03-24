import scrapy
import playwright

class ScrollSpider(scrapy.Spider):
    name = "scroll"

    def start_requests(self):
        yield scrapy.Request(
            url="http://quotes.toscrape.com/scroll",
            meta=dict(
                playwright=True,
                playwright_include_page=True,
                playwright_page_coroutines=[
                    PageCoroutine("wait_for_selector", "div.quote"),
                    PageCoroutine("evaluate", "window.scrollBy(0, document.body.scrollHeight)"),
                    PageCoroutine("wait_for_selector", "div.quote:nth-child(11)"),  # 10 per page
                ],
            ),
        )

    async def parse(self, response):
        page = response.meta["playwright_page"]
        await page.screenshot(path="quotes.png", fullPage=True)
        yield {"quote_count": len(response.css("div.quote"))}  # quotes from several pages
        await page.close()
