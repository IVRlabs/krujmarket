from django import forms
from .models import Category


class ProductFilterForm(forms.Form):
    category = forms.ModelChoiceField(
        queryset=Category.objects.none(),  # Пустой queryset по умолчанию
        required=False,
        label="Категория",
        widget=forms.Select(attrs={'class': 'form-select'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Динамически обновляем queryset
        self.fields['category'].queryset = Category.objects.filter(
            products__is_active=True
        ).distinct()