from rest_framework import serializers

from tables.models import Table


class TableSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'name', 'quantity', 'table_type')
        model = Table
