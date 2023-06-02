from time import sleep
from django.core.management.base import BaseCommand
from django.db import connection
from django.db.utils import OperationalError

class Command(BaseCommand):
    help = 'wait for db conection'

    def handle(self, *args, **options) -> str | None:
        self.stdout.write('waiting for db...')
        isConnect = False

        while not isConnect:
            try:
                c = connection.cursor()
                c.execute('SELECT 1')
                isConnect = True
            except OperationalError:
                self.stdout.write('Database unavailable, waitingin 1 second...')
                sleep(1)

        self.stdout.write(self.style.SUCCESS('Database available'))