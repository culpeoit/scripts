#!/usr/bin/python3
import logging  # For logging
import os       # For ping
import requests # For HTTP request

_logger = logging.getLogger(__name__)

def check_connectivity(site):
    # TODO swap os.system with subprocess.call
    ping = os.system("ping -n 1 " +site)

    if ping == 0:
        _logger.info('Site %s is online', site)
        return True
    else:
        _logger.warning('Site %s is down', site)
        return False


def check_service(service):
    # Makes HTTP request
    request = requests.get("https://"+service)

    if request.status_code != 200:
        _logger.warning("Service %s is down", service)
        return False
    else:
        _logger.info("Service %s is online", service)
        return True
