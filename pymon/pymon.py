import monitor
import report
import logging
import json
from datetime import datetime

_logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s [ %(levelname)s ] %(message)s', datefmt='%Y-%m-%d %H:%M:%S', filename='pymon.log', level=logging.INFO)

with open("sites.json", "r") as json_file:
    SITES = json.load(json_file)

def reporte():
    report.report_mail(SITES)    

def main():
    _logger.info("Starting PyMon main on: %s", datetime.now())
    for site in SITES:
        status = monitor.check_connectivity(site["ip"])
        # If no monitoring and online, enable monitoring
        if not site["online"] and status:
            _logger.info("Site %s is back online", site["name"])
            site["online"] = True

        # If monitoring and offline, disable monitoring
        if site["online"] and not status:
            _logger.info("Triggering alert for site %s", site["name"])
            report.alert(site)
            site["online"] = False
    with open("sites.json", "w") as json_file:
        json.dump(SITES, json_file)

if __name__ == '__main__':
    main()