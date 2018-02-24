import requests

def catchLines(lines, target, linesToGrab):
    splitLines = lines.splitlines()
    foundTarget = False
    caughtLines = []

    for line in splitLines:
        if target in line:
            foundTarget = True

        if foundTarget:
            if linesToGrab > 0:
                caughtLines.append(line)
                linesToGrab -= 1
            else:
                break

    return caughtLines

def sanitizeLines(caughtLines):
    textToStrip = [
        "<td valign=\"top\" class=\"rpt127\">",
        "</td>",
        "<td valign=\"top\" class=\"rpt127r\">"
    ]

    sanitizedLine = ""

    for line in caughtLines:
        strippedLine = line.strip()

        clearedLine = strippedLine

        for oneTextToStrip in textToStrip:
            clearedLine = clearedLine.replace(oneTextToStrip, "")

        if clearedLine != "":
            sanitizedLine += " " + clearedLine

    return sanitizedLine


def processLines(lines, year):
    target = "16.5"
    linesToGrab = 5
    
    caughtLines = catchLines(lines, target, linesToGrab)
    if len(caughtLines) > 0:
        sanitizedLine = sanitizeLines(caughtLines)
        print("{}: {}".format(year, sanitizedLine))
    else:
        print("{}: Did not find {}".format(year, target))


baseUrl = "https://cats.airports.faa.gov/Reports/reports.cfm"
startYear = 2009
endYear = 2017
pitAirportId = 2179
debug = False

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

    if debug:
        print("DEBUG: Posting \"{}\" with payload \"{}\"".format(postRequestUrl, payload))

    session = requests.Session()
    r = session.post(postRequestUrl, headers=headers, data=payload)

    if r.status_code == requests.codes.ok:
        processLines(r.text, currentYear)
    else:
        print("Status code \"{}\"!".format(r.status_code))
