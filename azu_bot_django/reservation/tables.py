from rest_framework import serializers

from tables.models import Table


def get_available_table(validated_data, reservation):
    cafe = validated_data.pop('cafe')
    quantity = validated_data.pop('quantity')
    date = validated_data.pop('date')
    unailable_tables = reservation.table.through.objects.filter(
        reservation__cafe__id=cafe.id,
        reservation__date=date,
        reservation__status=1
    ).values('table')
    if quantity == 1:
        available_bar_tables = Table.objects.select_for_update(
        ).filter(
            cafe__id=cafe.id,
            table_type='bar_table',
        ).exclude(
            id__in=unailable_tables
        )
        available_bar_tables = available_bar_tables.filter(
            quantity__gte=1).first()
        if available_bar_tables:
            reservation.table.add(available_bar_tables)
            return
    available_simple_tables = Table.objects.select_for_update().filter(
        cafe__id=cafe.id,
        table_type='simple_table',
    ).exclude(
        id__in=unailable_tables
    )
    available_bar_tables = Table.objects.select_for_update().filter(
        cafe__id=cafe.id,
        table_type='bar_table',
    ).exclude(
        id__in=unailable_tables
    )
    single_table = available_simple_tables.filter(
        quantity__gte=quantity).first()
    if single_table:
        reservation.table.add(single_table)
        return
    else:
        merged_tables = merge_tables(
            available_simple_tables, quantity)
        if merged_tables:
            reservation.table.set(merged_tables)
        else:
            reservation.delete()
            raise serializers.ValidationError(
                {
                    'status': 'error',
                    'message': 'Недостаточно свободных столов.'
                }
            )


def merge_tables(available_tables, required_quantity):
    available_tables = available_tables.order_by('-quantity')
    merged_tables = []
    total_quantity = 0
    for table in available_tables:
        merged_tables.append(table)
        total_quantity += table.quantity
        if total_quantity >= required_quantity:
            return merged_tables
    return None
