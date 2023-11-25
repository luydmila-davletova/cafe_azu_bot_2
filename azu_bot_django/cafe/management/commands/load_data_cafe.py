from csv import DictReader

from django.core.management import BaseCommand

from cafe.models import Cafe


class Command(BaseCommand):
    """Загрузка кафе из static/data/cafes.csv в базу данных"""
    help = "Loads data from csv files in static/data/cafes.csv"

    def handle(self, *args, **options):
        for cafes in DictReader(
            open('static/data/cafes.csv', encoding="utf8")
        ):
            cafe = Cafe(
                id=cafes['id'],
                name=cafes['name'],
                address=cafes['address'],
                number=cafes['number']
            )
            cafe.save()
