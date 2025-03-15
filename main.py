import json

import requests
from tabulate import tabulate

EVENT_ID = 7250556144618307584
RACE_ID = 491104
TESTING_ENABLED = False
LIMIT = 50


def build_url(event_id: int, race_id: int, offset: int, limit: int):
    url = f"https://eventresults-api.sporthive.com/api/events/{event_id}/races/{race_id}/classifications/search?count={limit}&offset={offset}"
    return url


def get_page_runners(page_url: str) -> list :
    page_response = requests.get(page_url)
    page_content = page_response.content
    page_data = json.loads(page_content)['fullClassifications']
    return page_data


def count_runners_per_country(runners: list) -> dict:
    runner_count_per_country = {}
    for runner in runners:
        country_code = runner['classification']['countryCode']
        if country_code in runner_count_per_country.keys():
            runner_count_per_country[country_code] += 1
        else:
            runner_count_per_country[country_code] = 1
    return runner_count_per_country


def sort_runners_per_country(runner_count_per_country: list) -> list:
    RUNNER_COUNT_INDEX = 1
    sorting_function = lambda country: country[RUNNER_COUNT_INDEX]
    runner_count_per_country.sort(
        key=sorting_function,
        reverse=True
    )
    return runner_count_per_country


def get_first_page_runners() -> list:
    first_page_url = build_url(
        event_id=EVENT_ID,
        race_id=RACE_ID,
        offset=0,
        limit=LIMIT
    )
    return get_page_runners(first_page_url)


def get_all_runners() -> list:
    runners = []
    all_runners_processed: bool = False
    offset: int = 0
    while not all_runners_processed:
        print(f"Getting page with runners from {offset} to {offset + LIMIT}")
        url = build_url(
            event_id=EVENT_ID,
            race_id=RACE_ID,
            offset=offset,
            limit=LIMIT
        )
        page_data = get_page_runners(url)
        runners.extend(page_data)
        offset += LIMIT
        all_runners_processed = (len(page_data) == 0)
    return runners


def print_table(table: list, headers: list):
    print(tabulate(table, headers=headers))


if __name__ == "__main__":
    if TESTING_ENABLED:
        data = get_first_page_runners()
    else:
        data = get_all_runners()

    runner_count_per_country_as_dict = count_runners_per_country(data)
    runner_count_per_country_as_list = [[country_code, runner_count] for (country_code, runner_count) in
                                        runner_count_per_country_as_dict.items()]

    sorted_countries = sort_runners_per_country(runner_count_per_country_as_list)

    print_table(
        table=sorted_countries,
        headers=['Country code', 'Runner count']
    )
