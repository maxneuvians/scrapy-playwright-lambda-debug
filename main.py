from scrapy import Request, Spider
from scrapy.crawler import CrawlerProcess


args = [
        '--no-sandbox',
        '--disable-setuid-sandbox',
        #'--single-process',
        '--no-zygote'
    ]


class UrlSpider(Spider):
    name = "url_spider"

    def start_requests(self):
        yield Request(
            url="https://example.org",
            meta={"playwright": True},
        )

    def parse(self, response):
        return response.url

def runner():
    runner = CrawlerProcess(
        settings={
            "CONCURRENT_REQUESTS": 1,
            "TWISTED_REACTOR": "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
            "DOWNLOAD_HANDLERS": {
                "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
                "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
            },
            "PLAYWRIGHT_LAUNCH_OPTIONS": {
                "args": args
            },
        }
    )
    runner.crawl(UrlSpider)
    runner.start()


def handler(event, context):
    runner()
    return args