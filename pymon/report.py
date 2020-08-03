import mailinfo
import smtplib
import logging

from datetime import datetime
from monitor import check_connectivity
from string import Template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

_logger = logging.getLogger(__name__)

MAIL_USER = mailinfo.mail_user
MAIL_PASS = mailinfo.mail_pass
MAIL_DEST = mailinfo.dest
MAIL_SERVER = mailinfo.smtp_server

def read_template(filename):
    with open(filename, 'r', encoding='utf-8') as template_file:
        template_file_content = template_file.read()
    return Template(template_file_content)


def alert(site):
    # Set up SMTP server
    _logger.info('Setting up SMTP server: %s', MAIL_SERVER)
    m = smtplib.SMTP_SSL(MAIL_SERVER, '465')
    m.login(MAIL_USER, MAIL_PASS)

    # Get template and format it
    _logger.info('Setting up template')
    message_template = read_template('msg_monitor.txt')
    message = message_template.substitute(HOST=site["name"], DATE_TIME=datetime.now())

    # Start message and attach template
    _logger.info('Starting message')
    msg = MIMEMultipart()
    msg.attach(MIMEText(message, 'plain'))

    # Set mail parameters
    msg['From']=MAIL_USER
    msg['Subject']="Monitor caido: "+site["name"]

    for mail in MAIL_DEST:
        _logger.info('Preparing mail for %s', mail)
        # Set mail destinator
        msg['To']=mail

        # Send mail
        _logger.info('Sending mail to %s', mail)
        m.send_message(msg)
    # Finish and quit session
    _logger.info('Ending SMTP session')
    m.quit()

def report_mail(sites):
    # Set up SMTP server
    m = smtplib.SMTP_SSL(MAIL_SERVER, '465')
    m.login(MAIL_USER, MAIL_PASS)
    
    # Get template and format it
    message_template = read_template('msg_report.txt')

    # Start message and attach template
    msg = MIMEMultipart()
    # Template header
    header_temp = read_template('msg_header.txt')
    header = header_temp.substitute(DATE=datetime.now())
    # Template footer
    footer_temp = read_template('msg_footer.txt')
    footer = footer_temp.substitute()
    # Attach header to message
    msg.attach(MIMEText(header, 'plain'))
    
    for site in sites:
        if site["online"]:
            status="Online"
        else:
            status="Offline"
        message = message_template.substitute(HOST=site["name"], STATUS=status)
        msg.attach(MIMEText(message, 'plain'))

    # Attach footer to message
    msg.attach(MIMEText(footer, 'plain'))
    # Set mail parameters
    msg['Subject']="Reporte diario del "+datetime.today()
    msg['From']=MAIL_USER

    for mail in MAIL_DEST:
        # Set mail destinator
        msg['To']=mail

        # Send mail
        m.send_message(msg)
    # Finish and quit session
    m.quit()