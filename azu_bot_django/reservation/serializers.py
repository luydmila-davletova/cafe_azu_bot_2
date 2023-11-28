from rest_framework import serializers
from django.db import transaction

from menu.serializers import SetReadSerializer
from reservation.models import OrderSets, Reservation
from tables.models import Table
from tables.serializers import TableSerializer


class OrderSetsSerializer(serializers.ModelSerializer):
    sets = SetReadSerializer

    class Meta:
        fields = 'sets', 'quantity'
        model = OrderSets


class ReservationWriteSerializer(serializers.ModelSerializer):
    quantity = serializers.IntegerField()
    sets = OrderSetsSerializer(many=True)

    class Meta:
        fields = ('id', 'quantity', 'sets', 'date', 'name', 'number')
        model = Reservation

    def create(self, validated_data):
        res_sets = validated_data.pop('sets')
        res_quantity = validated_data.pop('quantity')
        reservation = Reservation.objects.create(**validated_data)
        for res_set in res_sets:
            OrderSets.objects.create(
                reservation=reservation,
                sets=res_set['sets'],
                quantity=res_set['quantity']
            )
        validated_data['quantity'] = res_quantity
        self.get_available_table(validated_data, reservation)
        return reservation

    def get_available_table(self, validated_data, reservation):
        """
        Ищем доступные столы и создаем связь с бронью, либо выдаем ошибку
        """
        cafe = validated_data.pop('cafe')
        quantity = validated_data.pop('quantity')
        date = validated_data.pop('date')
        unailable_tables = reservation.table.through.objects.filter(
            reservation__cafe__id=cafe.id,
            reservation__date=date,
            reservation__status='booked'
        ).values('table')
        if quantity == 1:
            with transaction.atomic():
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
        with transaction.atomic():
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
            merged_tables = self.merge_tables(
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

    def merge_tables(self, available_tables, required_quantity):
        """Соединяем столы"""
        available_tables = available_tables.order_by('-quantity')
        merged_tables = []
        total_quantity = 0
        for table in available_tables:
            merged_tables.append(table)
            total_quantity += table.quantity
            if total_quantity >= required_quantity:
                return merged_tables
        return None


class ReservationReadSerializer(serializers.ModelSerializer):
    table = TableSerializer(many=True, read_only=True)
    sets = SetReadSerializer(many=True, read_only=True)

    class Meta:
        fields = ('id', 'table', 'sets', 'date', 'name', 'number', 'status')
        model = Reservation
