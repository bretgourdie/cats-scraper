import requests

def processLines(lines, year):
    splitLines = lines.splitlines()
    target = "16.5"
    foundTarget = False

    for line in splitLines:
        if target in line:
            foundTarget = True
            print("{}: {}".format(year, line))

    if not foundTarget:
        print("{}: Did not find {}".format(year, target))

baseUrl = "https://cats.airports.faa.gov/Reports/reports.cfm"
startYear = 2009
endYear = 2017
pitAirportId = 2179

for currentYear in range(startYear, endYear + 1):
    postRequestUrl = "https://cats.airports.faa.gov/Reports/rpt127.cfm"
    headers = {"User-Agent": "Mozilla/5.0"}
    payload = {
        "AirportName": str(pitAirportId),
        "AirportId": str(pitAirportId),
        "State": "0",
        "RegionId": "0",
        "Year": str(currentYear),
        "view": "Screen",
        "YearToCompare": "0"
    }

    print("Posting \"{}\"".format(postRequestUrl))

    session = requests.Session()
    r = session.post(postRequestUrl, headers=headers, data=payload)

    if r.status_code == requests.codes.ok:
        processLines(r.text, currentYear)
    else:
        print("Status code \"{}\"!".format(r.status_code))
