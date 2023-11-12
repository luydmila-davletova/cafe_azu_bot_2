from django import forms

from reservation.models import Reservation
from menu.models import Set, Dishes
from cafe.models import Cafe


class BookingForm(forms.ModelForm):
    set = forms.ModelChoiceField(queryset=Set.objects.all())
    quantity = forms.IntegerField()

    class Meta:
        model = Reservation
        fields = ['date', 'cafe', 'name', 'number']


class ComboForm(forms.ModelForm):
    class Meta:
        model = Set
        fields = ['name', 'description', 'dishes', 'price']

    def validate_price(self):
        price = self.cleaned_data.get('price')
        if price is not None and price <= 0:
            raise forms.ValidationError("Цена должна быть больше нуля.")
        return price


class DishesForm(forms.ModelForm):
    class Meta:
        model = Dishes
        fields = ['name', 'description']


class LocationForm(forms.ModelForm):
    class Meta:
        model = Cafe
        fields = ['name', 'address']
