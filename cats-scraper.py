import requests
import collections
import csv
from CatsConfig import CatsConfig
import json

def createCsv(dataHeaders, dataByYearsByAirport):
    filename = "cats_data.csv"

    with open(filename, "w", newline="") as csvfile:
        writer = csv.writer(
            csvfile,
            delimiter=",",
            quotechar="|",
            quoting=csv.QUOTE_MINIMAL)
        
        writer.writerow(["Years"] + dataHeaders)

        for airport, statsByYear in dataByYearsByAirport.items():
            orderedStatsByYear = collections.OrderedDict(sorted(statsByYear.items()))
            for year, data in orderedStatsByYear.items():

                writer.writerow([year] + data)

def processResponse(response, year, airport):
    decoded = response.content.decode("utf-8")

    reader = csv.reader(decoded.splitlines(), delimiter=",")

    rows = list(reader)

    if len(rows) == 4:
        title = rows[0]
        retrievalTime = rows[1]
        headers = rows[2]
        data = rows[3]

        return headers, data

    else:
        print("Year {} was not found for airport {}.".format(year, airport))
        return None, None



config = CatsConfig()

debug = False

yearsByAirport = {}

statsHeaders = []

airports = config.AirportId.split(",")

for airport in airports:

    statsByYear = {}

    for currentYear in range(config.StartYear, config.EndYear + 1):
        postRequestUrl = "https://cats.airports.faa.gov/Reports/rpt127.cfm"
        headers = {"User-Agent": "Mozilla/5.0"}
        payload = {
            "AirportName": str(airport),
            "AirportId": str(airport),
            "State": str(config.State),
            "RegionId": str(config.RegionId),
            "Year": str(currentYear),
            "view": config.view,
            "YearToCompare": str(config.YearToCompare)
        }

        if debug:
            print("DEBUG: Posting \"{}\" with payload \"{}\"".format(postRequestUrl, payload))

        session = requests.Session()
        r = session.post(postRequestUrl, headers=headers, data=payload)

        if r.status_code == requests.codes.ok:
            headers, data = processResponse(r, currentYear, airport)

            if headers != None and data != None:
                statsHeaders = headers
                statsByYear[currentYear] = data
        else:
            print("Status code \"{}\"!".format(r.status_code))

    yearsByAirport[airport] = statsByYear

createCsv(headers, yearsByAirport)
