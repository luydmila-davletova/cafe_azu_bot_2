from django import forms

from menu.models import Dishes, Set


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
