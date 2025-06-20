from django import forms
from .models import Order

class OrderCreateForm(forms.Form):
    first_name = forms.CharField(label='Имя', required=True)
    last_name = forms.CharField(label='Фамилия', required=True)
    email = forms.EmailField(label='Email', required=True)
    phone = forms.CharField(label='Телефон', required=True)
    address = forms.CharField(label='Адрес', required=True)
    city = forms.CharField(label='Город', required=True)
    postal_code = forms.CharField(label='Почтовый индекс', required=False)
    comments = forms.CharField(label='Комментарий', widget=forms.Textarea, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
            