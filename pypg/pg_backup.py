#!/usr/bin/python3
import logging			# Import logging
import confidential_vars	# Import sensitive info
from sh import pg_dump		# Import pg_dump for backup

WORKDIR = "/scripts/pypg/"
BACKUP_PATH = "/backup/postgres/"
DATABASES = confidential_vars.databases
PG_USER = confidential_vars.pg_user

_logger = logging.getLogger(__name__)

logging.basicConfig(format='%(asctime)s [ %(levelname)s ] %(message)s', datefmt='%Y-%m-%d %H:%M:%S', filename='/var/logs/scripts/pypg.log', level=logging.INFO)

def main():
        
        _logger.info('Starting process for databases backup')

        if len(DATABASES) == 0:
                try:
                        # Raise exception if databases field is empty
                        raise NameError('No databases') 
                except NameError:
                        _logger.exception('No databases to backup')
                        raise

        for db in DATABASES:
                _logger.info('Starting backup of database: %s', db)
                uri = ('--dbname=postgres://%s@localhost/%s?passfile=%s.pgpass' % (PG_USER, db, WORKDIR))	# Set URI with passfile as pg_dump doesn't accept hardcoded passwords
                pg_dump(uri,
                        '--no-privileges',	# No privileges and no owner to avoid permissions conflicts
                        '--no-owner',
                        '-f', BACKUP_PATH +db +'.backup',	# Output file
                        )

        _logger.info('Ending database backup process')


if __name__ == '__main__':
    main()