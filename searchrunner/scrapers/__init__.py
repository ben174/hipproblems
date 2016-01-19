from searchrunner.scrapers.expedia import ExpediaScraper
from searchrunner.scrapers.orbitz import OrbitzScraper
from searchrunner.scrapers.priceline import PricelineScraper
from searchrunner.scrapers.travelocity import TravelocityScraper
from searchrunner.scrapers.united import UnitedScraper


SCRAPERS = [
    ExpediaScraper,
    OrbitzScraper,
    PricelineScraper,
    TravelocityScraper,
    UnitedScraper,
]
SCRAPER_MAP = {s.provider.lower(): s for s in SCRAPERS}


def get_scraper(provider):
    return SCRAPER_MAP.get(provider.lower())
