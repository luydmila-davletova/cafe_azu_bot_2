from django import forms
from django.db import models

from cafe.models import Cafe
from menu.models import Dishes, Set
from reservation.models import Reservation
from tables.models import Table


class BookingForm(forms.ModelForm):
    set = forms.ModelChoiceField(queryset=Set.objects.all())
    quantity = forms.IntegerField()

    class Meta:
        model = Reservation
        fields = ['date', 'cafe', 'name', 'number']

    def clean_quantity(self):
        cafe = self.cleaned_data.get('cafe')
        quantity = self.cleaned_data.get('quantity')
        if cafe and quantity:
            total_table_capacity = Table.objects.filter(
                cafe=cafe).aggregate(
                    models.Sum('quantity'))['quantity__sum']
            if total_table_capacity and quantity > total_table_capacity:
                raise forms.ValidationError('Превышение допустимого кол-ва.')
        return quantity


class ComboForm(forms.ModelForm):
    class Meta:
        model = Set
        fields = ['name', 'description', 'dishes', 'price']

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None and price <= 0:
            raise forms.ValidationError('Цена должна быть больше нуля.')
        return price


class DishesForm(forms.ModelForm):
    class Meta:
        model = Dishes
        fields = ['name', 'description']


class LocationForm(forms.ModelForm):
    class Meta:
        model = Cafe
        fields = ['name', 'address']


class TableForm(forms.ModelForm):
    TABLE_TYPE_CHOICES = [
        ('simple_table', 'Простой стол'),
        ('bar_table', 'Барный стол')
    ]
    table_type = forms.ChoiceField(
        choices=TABLE_TYPE_CHOICES,
        label='Тип места'
    )

    class Meta:
        model = Table
        fields = ['name', 'cafe', 'table_type', 'quantity']

    quantity = forms.IntegerField(label='Количество', initial=1)

    def clean(self):
        cleaned_data = super().clean()
        table_type = cleaned_data.get('table_type')
        quantity = cleaned_data.get('quantity')

        if table_type == 'bar_table' and quantity != 1:
            raise forms.ValidationError(
                'Барное место может быть только = 1')
        return cleaned_data
