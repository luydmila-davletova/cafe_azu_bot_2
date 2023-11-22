from rest_framework import serializers

from menu.models import Dishes, Set, SetDish

# from rest_framework.validators import UniqueTogetherValidator



class DishesSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Dishes


class SetDishSerializer(serializers.ModelSerializer):
    dish = DishesSerializer

    class Meta:
        fields = 'dish', 'quantity'
        model = SetDish


class SetReadSerializer(serializers.ModelSerializer):
    dishes = DishesSerializer(many=True, read_only=True)

    class Meta:
        fields = '__all__'
        model = Set


class SetWriteSerializer(serializers.ModelSerializer):
    dishes = SetDishSerializer(many=True, write_only=True)

    class Meta:
        fields = '__all__'
        model = Set

    def create(self, validated_data):
        set_dishes = validated_data.pop('dishes')
        set = Set.objects.create(**validated_data)
        for set_dish in set_dishes:
            SetDish.objects.create(
                dish=set_dish['dish'],
                set=set,
                quantity=set_dish['quantity']
            )
        return set

    def validate(self, data):
        price = data.get('price')
        if price <= 0:
            raise serializers.ValidationError('Цена должна быть больше нуля.')
        return data
