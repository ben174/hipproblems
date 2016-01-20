# Building a Flight Search API

When a user does a flight search on Hipmunk we search many partner sites simultaneously to ensure we give them the best options. In this problem, you'll build an API that queries each of our different partners and merges their results together.

# Background

Hipmunk has a scraper farm that we use to search our partner sites. The name scraper is a legacy holdover from when we actually scraped them. Nowadays, we query their APIs :)

For this problem, the scraper farm will be emulated by a simple web server.

To start it, run `python -m searchrunner.scraperapi`. This should start a server listening on port 9000.

This server exposes exactly one endpoint: `/scrapers/<provider>` which will return the flight results from that provider as JSON.

Here are the providers that are available:

- Expedia
- Orbitz
- Priceline
- Travelocity
- United

# The Problem

Your job is to build an API that queries each provider and returns a merged list containing all of their results.

Requirements:
- You must search all providers
- The results should be sorted by agony
- The scraper APIs already return results sorted by agony, you should take advantage of this!

You may write your API in whatever language you want. It should run on port 8000 and expose exactly one endpoint: `/flights/search` which should return a JSON response. The JSON response should look identical to the scraper API response except that it will contain results from all providers, sorted by agony.
