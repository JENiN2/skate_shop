from django import forms
from .models import Skate


class SkateForm(forms.Form):
    name = forms.CharField(
        max_length=50,
        min_length=2,
        strip=True,  # strip убирает пробелы в начале и конце
        label='Название скейта'
        )
    description = forms.CharField(
        max_length=155,
        min_length=2,
        strip=True,
        label='Описание скейта',
        widget=forms.Textarea,
        initial='Описание',
        )
    price = forms.FloatField(
        min_value=1,
        label='Цена скейта',
        initial=40
        )
    article_number = forms.IntegerField(
        label='Артикул товара',
        )
    color = forms.CharField(
        max_length=30,
        min_length=2,
        strip=True,
        label='Цвет скейта',
        initial='Цвет',
    )
    photo = forms.ImageField(
        required=False,
        label='Фото скейта'
        )


class SkateUpdForm(forms.ModelForm):

    class Meta:
        model = Skate  # модель берет поля формы
        fields = ['name', 'description', 'price', 'article_number', 'color', 'photo', 'exist']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control',
                                            'id': 'floatingInput'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'article_number': forms.NumberInput(attrs={'class': 'form-control'}),
            'color': forms.TextInput(attrs={'class': 'form-control'}),
            'exist': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
