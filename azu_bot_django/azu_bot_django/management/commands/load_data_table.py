from csv import DictReader

from django.core.management import BaseCommand
from tables.models import Table
from cafe.models import Cafe


class Command(BaseCommand):
    """Загрузка столов из static/data/tables.csv в базу данных"""
    help = "Loads data from csv files in static/data/tables.csv"

    def handle(self, *args, **options):
        for tables in DictReader(
            open('static/data/tables.csv', encoding="utf8")
        ):
            table = Table(
                name=tables['name'],
                cafe=Cafe.objects.get(id=tables['cafe']),
                quantity=tables['quantity'],
                table_type=tables['table_type']
            )
            table.save()
