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

startYear = 2009
endYear = 2017

baseUrl = "https://cats.airports.faa.gov/Reports/reports.cfm"

pitAirportId = 2179

for currentYear in range(startYear, endYear + 1):
    getRequestUrl = "https://cats.airports.faa.gov/Reports/reports.cfm?AirportID={}&Year={}".format(pitAirportId, currentYear)

    print("Getting \"{}\"".format(getRequestUrl))

    r = requests.post(getRequestUrl)

    if r.status_code == requests.codes.ok:
        processLines(r.text, currentYear)
    else:
        print("Status code \"{}\"!".format(r.status_code))
