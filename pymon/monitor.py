import mailinfo
import smtplib
import logging
import os
import requests
import hostsmon

from string import Template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime


MAIL_USER = mailinfo.mail_user
MAIL_PASS = mailinfo.mail_pass
MAIL_DEST = mailinfo.dest
MAIL_SERVER = mailinfo.smtp_server
SITES = hostsmon.sites
SERVICES = hostsmon.services

logging.basicConfig(filename='log.txt', level=logging.INFO)

def read_template(filename):
    with open(filename, 'r', encoding='utf-8') as template_file:
        template_file_content = template_file.read()
    return Template(template_file_content)

def check_connectivity(site):
    # Makes ping check
    ping = os.system("ping -n 1 " +site)

    if ping == 1:
        logging.warning('Site %s is down', site)
        alert(site)
        # TODO: Add a followup ping until connectivity is recovered
    else:
        logging.info('Site %s is online', site)

def check_service(service):
    # Makes HTTP request
    request = requests.get("https://"+service)

    if request.status_code != 200:
        logging.warning("Service %s is down", service)
        alert(service)
    else:
        logging.info("Service %s is online", service)

def alert(site):
    # Set up SMTP server
    logging.info('Setting up SMTP server: %s', MAIL_SERVER)
    m = smtplib.SMTP_SSL(MAIL_SERVER, '465')
    m.login(MAIL_USER, MAIL_PASS)

    # Get template and format it
    logging.info('Setting up template')
    message_template = read_template('msg_monitor.txt')
    message = message_template.substitute(HOST=site, DATE_TIME=datetime.now())

    # Start message and attach template
    logging.info('Starting message')
    msg = MIMEMultipart()
    msg.attach(MIMEText(message, 'plain'))

    # Set mail parameters
    msg['From']=MAIL_USER
    msg['Subject']="Monitor caido: "+site

    for mail in MAIL_DEST:
        logging.info('Preparing mail for %s', mail)
        # Set mail destinator
        msg['To']=mail

        # Send mail
        logging.info('Sending mail to %s', mail)
        m.send_message(msg)
    # Finish and quit session
    logging.info('Ending SMTP session')
    m.quit()

def main():
    for site in SITES:
        check_connectivity(site)
    for service in SERVICES:
        check_service(service)

if __name__ == '__main__':
    main()
