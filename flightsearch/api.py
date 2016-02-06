import urlparse
import logging
import threading

import requests
import flask

app = flask.Flask(__name__)

SEARCH_RUNNER_ENDPOINT = 'http://localhost:9000/scrapers/'

SCRAPERS = [
    'Expedia',
    'Orbitz',
    'Priceline',
    'Travelocity',
    'United',
]


@app.route("/flights/search", methods=['GET'])
def flight_search():
    ret = {'results': None}
    result_groups = []
    threads = []
    for url in get_scraper_urls():
        thread = threading.Thread(
            target=get_results,
            args=(url, result_groups)
        )
        thread.daemon = True
        thread.start()
        threads.append(thread)
    # wait for all threads to return
    for t in threads:
        t.join()
    # merge the results into a master list
    all_results = merge_results(result_groups)
    ret['results'] = all_results
    return flask.jsonify(ret)


def get_scraper_urls():
    for scraper in SCRAPERS:
        yield urlparse.urljoin(SEARCH_RUNNER_ENDPOINT, scraper)


def get_results(url, result_groups):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        logging.error('Response {} from endpoint: {}'.format(
            response.status_code,
            url
        ))
        return
    data = response.json()
    if not 'results' in data.keys():
        logging.error('Invalid response from endpoint: {}'.format(url))
        return
    result_groups.append(data['results'])


def merge_results(result_groups):
    # iterates through each providers result sets, plucking the result
    # with the lowest agony, and adding that result to a master result
    # set
    results = []
    while result_groups:
        group = lowest_agony_group(result_groups)
        results.append(group.pop(0))
        # remove empty groups
        result_groups = [rg for rg in result_groups if rg != []]
    return results


def lowest_agony_group(groups):
    # scan the top record for each group to get the min agony
    min_agony = min([rg[0]['agony'] for rg in groups])
    for group in groups:
        if group[0]['agony'] == min_agony:
            return group


if __name__ == "__main__":
    app.run(debug=True, port=8000)
