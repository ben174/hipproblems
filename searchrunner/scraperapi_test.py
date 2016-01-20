from collections import Counter
import requests


EXPECTED_COUNTS = {
    "Expedia": 1199,
    "Orbitz": 300,
    "Priceline": 600,
    "Travelocity": 400,
    "United": 1799,
}


def test_flight_search():
    resp = requests.get("http://localhost:8000/flights/search")
    results = resp.json()["results"]

    provider_counts = Counter()
    for result in results:
        provider_counts[result["provider"]] += 1

    for provider, count in provider_counts.most_common():
        expected = EXPECTED_COUNTS[provider]
        assert count == expected, "%s results missing for %s" % (
            expected - count,
            provider,
        )

    sorted_results = sorted(results, key=lambda r: r["agony"])
    assert results == sorted_results, "Results aren't sorted properly!"

    took = resp.elapsed.total_seconds()

    msg = "Took %.2f seconds." % took
    if took > 3:
        msg += " Kinda slow..."
    else:
        msg += " Looks good!"

    print msg


if __name__ == "__main__":
    test_flight_search()
