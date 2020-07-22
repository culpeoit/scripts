import logging			# Import logging
import confidential_vars	# Import sensitive info
from sh import pg_dump		# Import pg_dump for backup

logging.basicConfig(filename='logs/db_backup.log', level=logging.INFO)
logging.info('Starting process for databases backup')

if len(confidential_vars.databases) == 0:
        logging.error('No databases to backup')
        raise NameError('No databases to backup found') # Raise exception if databases field is empty

for db in confidential_vars.databases:
        logging.info('Starting backup of database: %s', db)
        uri = ('--dbname=postgres://%s@localhost/%s?passfile=.pgpass' % (confidential_vars.pg_user,db))	# Set URI with passfile as pg_dump doesn't accep hardcoded passwords
        pg_dump(uri,
                '--no-privileges',	# No privileges and no owner to avoid permissions conflicts
                '--no-owner',
                '-f', db+'.backup',	# Output file
                )

logging.info('Ending database backup process')
