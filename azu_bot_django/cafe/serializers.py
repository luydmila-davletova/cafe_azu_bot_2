from rest_framework import serializers

from cafe.models import Cafe


class CafeSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Cafe
