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
                'required': 'True',
                'class': 'textinput',
                'minlength': 6,
                'maxlength': 30,
            }),
            "passwordhash": PasswordInput(attrs={
                'placeholder': 'Пароль',
                'required': 'True',
                'class': 'textinput',
                'minlength': 6,
                'maxlength': 30,
            }),
            "lastname": TextInput(attrs={
                'placeholder': 'Фамилия',
                'required': 'True',
                'class': 'textinput',
                'maxlength': 30,
            }),
            "firstname": TextInput(attrs={
                'placeholder': 'Имя',
                'required': 'True',
                'class': 'textinput',
                'maxlength': 30,
            }),
            "patronymic": TextInput(attrs={
                'placeholder': 'Отчество (при наличии)',
                'class': 'textinput',
                'maxlength': 30,
            }),
            "phonenumber": TextInput(attrs={
                'placeholder': 'Номер телефона',
                'required': 'True',
                'class': 'textinput',
            }),
        }


class LoginForm(Form):
    login = CharField(max_length=30, widget=TextInput(attrs={
        'placeholder': 'Логин',
        'required': 'True',
        'class': 'textinput',
        'minlength': 6,
        'maxlength': 30,
    }))
    password = CharField(max_length=30, widget=PasswordInput(attrs={
        'placeholder': 'Пароль',
        'required': 'True',
        'class': 'textinput',
        'minlength': 6,
        'maxlength': 30,
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