from tornado import ioloop, web
from searchrunner.scrapers import get_scraper


class ScraperApiHandler(web.RequestHandler):

    def get(self, provider):
        scraper_cls = get_scraper(provider)
        if not scraper_cls:
            self.set_status(400)
            self.write({
                "error": "Unkown provider",
            })
            return

        scraper = scraper_cls()
        results = scraper.run()
        self.write({
            "results": [r.serialize() for r in results],
        })


ROUTES = [
    (r"/scrapers/(?P<provider>\w+)", ScraperApiHandler),
]


def run():
    app = web.Application(
        ROUTES,
        debug=True,
    )
    app.listen(9000)
    ioloop.IOLoop.current().start()


if __name__ == "__main__":
    run()
