import requests

startYear = 2009
endYear = 2017

baseUrl = "https://cats.airports.faa.gov/Reports/reports.cfm"

pitAirportId = 2179

for currentYear in range(startYear, endYear):
    getRequestUrl = "https://cats.airports.faa.gov/Reports/reports.cfm?AirportID={}&Year={}".format(pitAirportId, currentYear)

    print("Getting \"{}\"".format(getRequestUrl))

    r = requests.post(getRequestUrl)

    if r.status_code == requests.codes.ok:
        print(r.text)
    else:
        print("Status code \"{}\"!".format(r.status_code))
