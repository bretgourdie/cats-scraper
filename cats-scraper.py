import requests
from CatsConfig import CatsConfig

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


def processLines(lines, year, target, linesToGrab):
    
    caughtLines = catchLines(lines, target, linesToGrab)
    if len(caughtLines) > 0:
        sanitizedLine = sanitizeLines(caughtLines)
        print("{}: {}".format(year, sanitizedLine))
    else:
        print("{}: Did not find {}".format(year, target))

config = CatsConfig()

debug = False

for currentYear in range(config.StartYear, config.EndYear + 1):
    postRequestUrl = "https://cats.airports.faa.gov/Reports/rpt127.cfm"
    headers = {"User-Agent": "Mozilla/5.0"}
    payload = {
        "AirportName": str(config.AirportId),
        "AirportId": str(config.AirportId),
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
        processLines(r.text, currentYear, config.Section, int(config.LinesToGrab))
    else:
        print("Status code \"{}\"!".format(r.status_code))
