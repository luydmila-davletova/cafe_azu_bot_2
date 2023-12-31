from csv import DictReader

from django.core.management import BaseCommand
from cafe.models import Cafe
from tables.models import Table
from menu.models import Dishes, Set


class Command(BaseCommand):
    """Загрузка данных из static/data в базу данных"""
    help = "Loads data from csv files in static/data"

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

        for dishes in DictReader(
            open('static/data/dishes.csv', encoding="utf8")
        ):
            dish = Dishes(
                id=dishes['id'],
                name=dishes['name'],
                description=dishes['description'],
                image=dishes['image']
            )
            dish.save()
        id_setdish = 1
        for cafe_sets in DictReader(
            open('static/data/sets.csv', encoding="utf8")
        ):
            cafe_set = Set(
                id=cafe_sets['id'],
                name=cafe_sets['name'],
                description=cafe_sets['description'],
                price=cafe_sets['price'],
                image=cafe_sets['image']
            )
            cafe_set.save()
            for dish in cafe_sets['dishes'].split(','):
                cafe_set.setdish_set.create(
                    id=id_setdish,
                    set=cafe_set,
                    dish=Dishes.objects.get(id=dish)
                )
                id_setdish += 1
