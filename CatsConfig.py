import configparser

class CatsConfig:

    def __init__(self, section="DEFAULT"):
        configFileName = "cats-scraper.ini"

        config = configparser.ConfigParser()
        config.read(configFileName)

        targetSection = config[section]

        self.Section = targetSection["Section"]
        self.ReportUrl = targetSection["ReportUrl"]
        self.StartYear = int(targetSection["StartYear"])
        self.EndYear = int(targetSection["EndYear"])
        self.AirportId = targetSection["AirportId"]
        self.State = int(targetSection["State"])
        self.RegionId = int(targetSection["RegionId"])
        self.view = targetSection["view"]
        self.YearToCompare = int(targetSection["YearToCompare"])
