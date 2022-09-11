# curl 'https://ariela-primo.hosted.exlibrisgroup.com/primo_library/libweb/webservices/rest/primo-explore/v1/pnxs?blendFacetsSeparately=false&getMore=0&inst=972SZA&lang=iw_IL&limit=10&mode=advanced&newspapersActive=false&newspapersSearch=false&offset=0&pcAvailability=true&q=sub,contains,%D7%AA%D7%97%D7%91%D7%95%D7%A8%D7%94+%D7%A6%D7%99%D7%91%D7%95%D7%A8%D7%99%D7%AA,AND&qExclude=&qInclude=facet_searchcreationdate,exact,%5B2020+TO+2020%5D&refEntryActive=false&rtaLinks=true&scope=default_scope&searchInFulltextUserSelection=true&skipDelivery=Y&sort=rank&tab=default_tab&vid=972SZA_PRESS' \
#   -H 'Accept: application/json, text/plain, */*' \
#   -H 'Accept-Language: en-US,en;q=0.9,he-IL;q=0.8,he;q=0.7' \
#   -H 'Authorization: Bearer eyJraWQiOiJwcmltb0V4cGxvcmVQcml2YXRlS2V5LTk3MlNaQSIsImFsZyI6IkVTMjU2In0.eyJpc3MiOiJQcmltbyIsImp0aSI6IiIsImV4cCI6MTY1NDQ5MzA2MSwiaWF0IjoxNjU0NDA2NjYxLCJ1c2VyIjoiYW5vbnltb3VzLTA2MDVfMDUyNDIxIiwidXNlck5hbWUiOm51bGwsInVzZXJHcm91cCI6IkdVRVNUIiwiYm9yR3JvdXBJZCI6bnVsbCwidWJpZCI6bnVsbCwiaW5zdGl0dXRpb24iOiI5NzJTWkEiLCJ2aWV3SW5zdGl0dXRpb25Db2RlIjoiOTcyU1pBIiwiaXAiOiIxNDcuMjM1LjE5NS41NyIsInBkc1JlbW90ZUluc3QiOm51bGwsIm9uQ2FtcHVzIjoiZmFsc2UiLCJsYW5ndWFnZSI6Iml3X0lMIiwiYXV0aGVudGljYXRpb25Qcm9maWxlIjoiIiwidmlld0lkIjoiOTcyU1pBX1BSRVNTIiwiaWxzQXBpSWQiOm51bGwsInNhbWxTZXNzaW9uSW5kZXgiOiIiLCJqd3RBbHRlcm5hdGl2ZUJlYWNvbkluc3RpdHV0aW9uQ29kZSI6Ijk3MlNaQSJ9.XqsI9ltIcewqeMngueuQNgUKSPHgoLbV3Ji2BDvS3z0lS4G0GVEer8h-s5cbBTwKoTkp65kICgk-82zdMPZ8pw' \
#   -H 'Connection: keep-alive' \
#   -H 'Cookie: JSESSIONID=12E293A51AA5EE99E6AD33A370218264; __Secure-UqZBpD3n3i7IBXwkmkSvpHGZA+oH-YtEPoiT69DFuAs_=v1p6o+gw__nfk' \
#   -H 'Referer: https://ariela-primo.hosted.exlibrisgroup.com/primo-explore/search?query=sub,contains,%D7%AA%D7%97%D7%91%D7%95%D7%A8%D7%94%20%D7%A6%D7%99%D7%91%D7%95%D7%A8%D7%99%D7%AA,AND&tab=default_tab&search_scope=default_scope&vid=972SZA_PRESS&mode=advanced&offset=0' \
#   -H 'Sec-Fetch-Dest: empty' \
#   -H 'Sec-Fetch-Mode: cors' \
#   -H 'Sec-Fetch-Site: same-origin' \
#   -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36' \
#   -H 'sec-ch-ua: " Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"' \
#   -H 'sec-ch-ua-mobile: ?0' \
#   -H 'sec-ch-ua-platform: "macOS"' \
#   --compressed

# https://curlconverter.com/
import csv
import json

import requests


class HttpError(Exception):
    pass


def get_facet_values(year, desired_facet="local1"):
    cookies = {
        'JSESSIONID': '12E293A51AA5EE99E6AD33A370218264',
        '__Secure-UqZBpD3n3i7IBXwkmkSvpHGZA+oH-YtEPoiT69DFuAs_': 'v1p6o+gw__nfk',
    }
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9,he-IL;q=0.8,he;q=0.7',
        'Authorization': 'Bearer eyJraWQiOiJwcmltb0V4cGxvcmVQcml2YXRlS2V5LTk3MlNaQSIsImFsZyI6IkVTMjU2In0.eyJpc3MiOiJQcmltbyIsImp0aSI6IiIsImV4cCI6MTY1NDQ5MzA2MSwiaWF0IjoxNjU0NDA2NjYxLCJ1c2VyIjoiYW5vbnltb3VzLTA2MDVfMDUyNDIxIiwidXNlck5hbWUiOm51bGwsInVzZXJHcm91cCI6IkdVRVNUIiwiYm9yR3JvdXBJZCI6bnVsbCwidWJpZCI6bnVsbCwiaW5zdGl0dXRpb24iOiI5NzJTWkEiLCJ2aWV3SW5zdGl0dXRpb25Db2RlIjoiOTcyU1pBIiwiaXAiOiIxNDcuMjM1LjE5NS41NyIsInBkc1JlbW90ZUluc3QiOm51bGwsIm9uQ2FtcHVzIjoiZmFsc2UiLCJsYW5ndWFnZSI6Iml3X0lMIiwiYXV0aGVudGljYXRpb25Qcm9maWxlIjoiIiwidmlld0lkIjoiOTcyU1pBX1BSRVNTIiwiaWxzQXBpSWQiOm51bGwsInNhbWxTZXNzaW9uSW5kZXgiOiIiLCJqd3RBbHRlcm5hdGl2ZUJlYWNvbkluc3RpdHV0aW9uQ29kZSI6Ijk3MlNaQSJ9.XqsI9ltIcewqeMngueuQNgUKSPHgoLbV3Ji2BDvS3z0lS4G0GVEer8h-s5cbBTwKoTkp65kICgk-82zdMPZ8pw',
        'Connection': 'keep-alive',
        # Requests sorts cookies= alphabetically
        # 'Cookie': 'JSESSIONID=12E293A51AA5EE99E6AD33A370218264; __Secure-UqZBpD3n3i7IBXwkmkSvpHGZA+oH-YtEPoiT69DFuAs_=v1p6o+gw__nfk',
        'Referer': 'https://ariela-primo.hosted.exlibrisgroup.com/primo-explore/search?query=sub,contains,%D7%AA%D7%97%D7%91%D7%95%D7%A8%D7%94%20%D7%A6%D7%99%D7%91%D7%95%D7%A8%D7%99%D7%AA,AND&tab=default_tab&search_scope=default_scope&vid=972SZA_PRESS&mode=advanced&offset=0',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
    }
    response = requests.get(
        f'https://ariela-primo.hosted.exlibrisgroup.com/primo_library/libweb/webservices/rest/primo-explore/v1/pnxs?blendFacetsSeparately=false&getMore=0&inst=972SZA&lang=iw_IL&limit=10&mode=advanced&newspapersActive=false&newspapersSearch=false&offset=0&pcAvailability=true&q=sub,contains,%D7%AA%D7%97%D7%91%D7%95%D7%A8%D7%94+%D7%A6%D7%99%D7%91%D7%95%D7%A8%D7%99%D7%AA,AND&qExclude=&qInclude=facet_searchcreationdate,exact,%5B{year}+TO+{year}%5D&refEntryActive=false&rtaLinks=true&scope=default_scope&searchInFulltextUserSelection=true&skipDelivery=Y&sort=rank&tab=default_tab&vid=972SZA_PRESS',
        cookies=cookies, headers=headers)

    if response.status_code != 200:
        print(f"Response status: {response.status_code}\nBody:\n{response.text}")
        raise HttpError()

    response_as_json = json.loads(response.text)
    facets_array = response_as_json.get("facets")
    if not (type(facets_array) is list):
        print(f"facets is not a list\nfacets:\n{facets_array}")
        raise HttpError()

    for facet in facets_array:
        facet_name = facet.get("name")
        print(f"facet_name={facet_name}")
        if facet_name == desired_facet:
            facet_values_array = facet.get("values")
            print(facet_values_array)
            return facet_values_array

    print("No facet! returning empty list")
    return []


def write_to_csv(to_csv):
    keys = to_csv[0].keys()
    with open('people.csv', 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(to_csv)


def create_ds():
    d = []
    for year in range(1993, 2022):
        print(f"Searching for year {year}")
        values_for_year = get_facet_values(year)
        for record in values_for_year:
            row = {"year": year, "value": record["value"], "count": record["count"]}
            d.append(row)
    write_to_csv(d)

import pandas as pd
# df = pd.read_csv('people.csv')


def normalize_paper_name(paper_name):
    if 'מעריב' in paper_name:
        return 'מעריב'
    if 'סופהשבוע' == paper_name:
        return 'מעריב'
    if 'הצופה' in paper_name:
        return 'הצופה'
    if 'הארץ' in paper_name:
        return 'הארץ'
    if 'ידיעות' in paper_name:
        return 'ידיעות'
    if 'יתד' in paper_name:
        return 'יתד'
    if 'מקור ראשון' in paper_name:
        return 'מקור ראשון'
    return paper_name


def normalize_paper_name_df(df):
    df = pd.read_csv('people.csv')
    df['normalize_newspaper_name'] = df.apply(lambda row: normalize_paper_name(row["value"]), axis=1)
    print(f'normalized paper names:\n{df["normalize_newspaper_name"].unique()}')
    df['count_normalized_newspaper_name'] = df.groupby(['normalize_newspaper_name', 'year'])['count'].transform(lambda x: x.sum())
    return df


def main():
    df = pd.read_csv('people.csv')
    df = normalize_paper_name_df(df)
    df.to_csv("with_normalize_paper_name.csv")
    df1 = df[['year', 'normalize_newspaper_name', 'count_normalized_newspaper_name']]
    df1 = df1.drop_duplicates()
    df1 = df1.rename({"normalize_newspaper_name": "newspaper", "count_normalized_newspaper_name": "count"}, axis=1)
    df1.to_csv("only_normalize_paper_name.csv")
    print(df1.head())
    df1.pivot_table('count', ['year'], 'newspaper').to_csv("pivot_paper_name.csv")




main()