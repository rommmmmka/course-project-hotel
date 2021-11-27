from .models import *
from django.forms import *


class DateInput(DateInput):
    input_type = 'date'


class RegisterForm(ModelForm):
    class Meta:
        model = Visitor
        fields = ["login", "passwordhash", "lastname", "firstname", "patronymic", "phonenumber"]
        widgets = {
            "login": TextInput(attrs={
                'placeholder': 'Логин',
                'required': 'True'
            }),
            "passwordhash": PasswordInput(attrs={
                'placeholder': 'Пароль',
                'required': 'True'
            }),
            "lastname": TextInput(attrs={
                'placeholder': 'Фамилия',
                'required': 'True'
            }),
            "firstname": TextInput(attrs={
                'placeholder': 'Имя',
                'required': 'True'
            }),
            "patronymic": TextInput(attrs={
                'placeholder': 'Отчество (при наличии)'
            }),
            "phonenumber": TextInput(attrs={
                'placeholder': 'Номер телефона',
                'required': 'True'
            }),
        }


class LoginForm(Form):
    login = CharField(max_length=30, widget=TextInput(attrs={
        'placeholder': 'Логин',
        'required': 'True',

    }))
    password = CharField(max_length=30, widget=PasswordInput(attrs={
        'placeholder': 'Пароль',
        'required': 'True',
    }))


class AddOrderForm(Form):
    checkindate = DateField(widget=DateInput(attrs={
        'placeholder': 'Дата заселения',
        'required': 'True',
    }))
    checkoutdate = DateField(widget=DateInput(attrs={
        'placeholder': 'Дата выселения',
        'required': 'True',
    }))
    numberofguests = IntegerField(min_value=1, max_value=4, widget=NumberInput(attrs={
        'placeholder': 'Количество проживающих',
        'required': 'True',
    }))