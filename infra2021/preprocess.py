import json
import os

import requests

import pandas as pd

NEWSPAPERS = {
    "Yedioth": {
        "filter_query": "lsr02,contains,ידיעות,AND"
    },
    "Haaretz": {
        "filter_query": "lsr02,contains,הארץ,AND"
    },
    "Maariv": {
        "filter_query": "lsr02,contains,מעריב,AND"
    },
    "Yated": {
        "filter_query": "lsr02,contains,יתד,AND"
    },
    "Makor": {
        "filter_query": "lsr02,contains,מקור ראשון,AND"
    }
}


class HttpError(Exception):
    pass


def request_to_catalog(q_param_value, q_include_param_value=""):
    cookies = {
        'JSESSIONID': '12E293A51AA5EE99E6AD33A370218264',
        '__Secure-UqZBpD3n3i7IBXwkmkSvpHGZA+oH-YtEPoiT69DFuAs_': 'v1p6o+gw__nfk',
    }
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9,he-IL;q=0.8,he;q=0.7',
        'Authorization': 'Bearer eyJraWQiOiJwcmltb0V4cGxvcmVQcml2YXRlS2V5LTk3MlNaQSIsImFsZyI6IkVTMjU2In0.eyJpc3MiOiJQcmltbyIsImp0aSI6IiIsImV4cCI6MTY1NDUwMjMxMSwiaWF0IjoxNjU0NDE1OTExLCJ1c2VyIjoiYW5vbnltb3VzLTA2MDVfMDc1ODMxIiwidXNlck5hbWUiOm51bGwsInVzZXJHcm91cCI6IkdVRVNUIiwiYm9yR3JvdXBJZCI6bnVsbCwidWJpZCI6bnVsbCwiaW5zdGl0dXRpb24iOiI5NzJTWkEiLCJ2aWV3SW5zdGl0dXRpb25Db2RlIjoiOTcyU1pBIiwiaXAiOiIxNDcuMjM1LjE5NS41NyIsInBkc1JlbW90ZUluc3QiOm51bGwsIm9uQ2FtcHVzIjoiZmFsc2UiLCJsYW5ndWFnZSI6Iml3X0lMIiwiYXV0aGVudGljYXRpb25Qcm9maWxlIjoiIiwidmlld0lkIjoiOTcyU1pBX1BSRVNTIiwiaWxzQXBpSWQiOm51bGwsInNhbWxTZXNzaW9uSW5kZXgiOiIiLCJqd3RBbHRlcm5hdGl2ZUJlYWNvbkluc3RpdHV0aW9uQ29kZSI6Ijk3MlNaQSJ9.a9odJ-Xp5ABVKjeG6jgrdGslS1bkjj1SDGeyt2p3ItHXcmMBgaDvwyFMzClusp7w-xGTD-RfY-gWqOkhtZIHYg',
        'Connection': 'keep-alive',
        # Requests sorts cookies= alphabetically
        # 'Cookie': 'JSESSIONID=12E293A51AA5EE99E6AD33A370218264; __Secure-UqZBpD3n3i7IBXwkmkSvpHGZA+oH-YtEPoiT69DFuAs_=v1p6o+gw__nfk',
        'Referer': 'https://ariela-primo.hosted.exlibrisgroup.com/primo-explore/search?query=lsr02,contains,%D7%99%D7%93%D7%99%D7%A2%D7%95%D7%AA%20%D7%90%D7%97%D7%A8%D7%95%D7%A0%D7%95%D7%AA,AND&query=sub,contains,%D7%AA%D7%97%D7%91%D7%95%D7%A8%D7%94%20%D7%A6%D7%99%D7%91%D7%95%D7%A8%D7%99%D7%AA,AND&tab=default_tab&search_scope=default_scope&sortby=rank&vid=972SZA_PRESS&lang=iw_IL&mode=advanced&offset=0',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
    }
    response = requests.get(
        f'https://ariela-primo.hosted.exlibrisgroup.com/primo_library/libweb/webservices/rest/primo-explore/v1/pnxs?blendFacetsSeparately=false&getMore=0&inst=972SZA&lang=iw_IL&limit=10&mode=advanced&newspapersActive=false&newspapersSearch=false&offset=0&pcAvailability=true&q={q_param_value}&qExclude=&qInclude=facet_searchcreationdate,exact,{q_include_param_value}&refEntryActive=false&rtaLinks=true&scope=default_scope&searchInFulltextUserSelection=true&skipDelivery=Y&sort=rank&tab=default_tab&vid=972SZA_PRESS',
        cookies=cookies, headers=headers)

    if response.status_code != 200:
        print(f"Response status: {response.status_code}\nBody:\n{response.text}")
        raise HttpError()

    return json.loads(response.text)


def year_to_q_include_param_value(year):
    return f"%5B{year}+TO+{year}%5D"


def total_by_newspaper_and_year(newspaper, year):
    response_from_catalog = request_to_catalog(NEWSPAPERS.get(newspaper).get("filter_query"),
                                               year_to_q_include_param_value(year))
    return response_from_catalog.get("info").get("total")


def total_public_transport_by_newspaper_and_year(newspaper, year):
    response_from_catalog = request_to_catalog(
        NEWSPAPERS.get(newspaper).get("filter_query") + ";any,contains,תחבורה ציבורית,AND",
        year_to_q_include_param_value(year))
    return response_from_catalog.get("info").get("total")


def facet_values_by_year(year, desired_facet):
    response_from_catalog = request_to_catalog("any,contains,תחבורה ציבורית,AND", year_to_q_include_param_value(year))
    facets_array = response_from_catalog.get("facets")
    for facet in facets_array:
        facet_name = facet.get("name")
        if facet_name == desired_facet:
            facet_values_array = facet.get("values")
            return facet_values_array
    print("No facet! returning empty list")
    return []


def create_normalized_newspaper_name_data_set():
    rows = []
    for newspaper in NEWSPAPERS.keys():
        print(f"Starting to query for {newspaper}...")
        for year in range(1993, 2023):
            print(f"\tStarting to query for {year}...")
            row = {
                "newspaper": newspaper,
                "year": year,
                "total_articles": total_by_newspaper_and_year(newspaper, year),
                "public_transport_articles": total_public_transport_by_newspaper_and_year(newspaper, year)
            }
            rows.append(row)
            print(row)
    return pd.DataFrame(rows)


def create_newspaper_type_data_set():
    rows = []
    for year in range(1993, 2023):
        print(f"\tStarting to query for {year}...")
        facet_values = facet_values_by_year(year, "local1")
        for facet_val in facet_values:
            row = {
                "year": year,
                "newspaper": facet_val.get("value"),
                "count": facet_val.get("count"),
            }
            rows.append(row)
    return pd.DataFrame(rows)


def get_newspaper_normalized_name(newspaper_name):
    if 'מעריב' in newspaper_name:
        return 'מעריב'
    if 'סופהשבוע' == newspaper_name:
        return 'מעריב'
    if 'הצופה' in newspaper_name:
        return 'הצופה'
    if 'הארץ' in newspaper_name:
        return 'הארץ'
    if 'ידיעות' in newspaper_name:
        return 'ידיעות'
    if 'יתד' in newspaper_name:
        return 'יתד'
    if 'מקור ראשון' in newspaper_name:
        return 'מקור ראשון'
    return newspaper_name


def articles_by_year_newspaper_detailed_name(csv_name):
    if os.path.isfile(f"raw_{csv_name}"):
        data_set = pd.read_csv(f"raw_{csv_name}")
    else:
        print("Creating dataset using API requests")
        data_set = create_newspaper_type_data_set()
        data_set.to_csv(f"raw_{csv_name}")
    data_set["newspaper_normalized_name"] = data_set.apply(lambda row: get_newspaper_normalized_name(row['newspaper']),
                                                           axis=1)
    data_set.to_csv("processed_" + csv_name)


def articles_by_year_newspaper_name(csv_name):
    if os.path.isfile(f"raw_{csv_name}"):
        data_set = pd.read_csv(f"raw_{csv_name}")
    else:
        print(f"Creating dataset for {csv_name} using API requests")
        data_set = create_normalized_newspaper_name_data_set()
        data_set.to_csv(f"raw_{csv_name}")

    total_for_year_data_set = data_set[["year", "total_articles", "public_transport_articles", "newspaper"]].groupby(['year']).agg({'total_articles': 'sum', 'public_transport_articles': 'sum'})
    total_for_year_data_set["public_transport_percentage"] = total_for_year_data_set["public_transport_articles"] / total_for_year_data_set["total_articles"]
    total_for_year_data_set.to_csv(f"total_{csv_name}")

    data_set["public_transport_percentage"] = data_set["public_transport_articles"] / data_set["total_articles"]
    data_set.to_csv(f"processed_{csv_name}")
    after_pivot = data_set.pivot_table('public_transport_percentage', ['year'], 'newspaper')
    after_pivot.to_csv(f"pivot_{csv_name}")


def main():
    articles_by_year_newspaper_name("public_transport_by_year_and_newspaper.csv")
    articles_by_year_newspaper_detailed_name("public_transport_by_year_and_newspaper_type.csv")



main()
