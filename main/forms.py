from .models import *
from django.forms import *


class DateInput(DateInput):
    input_type = 'date'


class RegisterForm(ModelForm):
    class Meta:
        model = Visitor
        fields = ["login", "passwordhash", "lastname", "firstname", "patronymic", "citizenship", "passport", "phonenumber"]
        widgets = {
            "login": TextInput(attrs={
                'placeholder': 'Логин',
                'required': 'True',
                'class': 'textinput',
                'minlength': 6,
                'maxlength': 30,
                'pattern': '[A-Za-z0-9_]+',
            }),
            "passwordhash": PasswordInput(attrs={
                'placeholder': 'Пароль',
                'required': 'True',
                'class': 'textinput',
                'minlength': 6,
                'maxlength': 30,
                'pattern': '[A-Za-z0-9_]+',
                'id': 'passinput1',
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
            "citizenship": TextInput(attrs={
                'placeholder': 'Гражданство',
                'required': 'True',
                'class': 'textinput',
                'maxlength': 30,
            }),
            "passport": TextInput(attrs={
                'placeholder': 'Серия и номер паспорта',
                'required': 'True',
                'class': 'textinput',
                'maxlength': 15,
            }),
            "phonenumber": TextInput(attrs={
                'placeholder': 'Номер телефона',
                'required': 'True',
                'class': 'textinput',
                'id': 'phonenumber',
                'maxlength': 19,
            }),
        }


class LoginForm(Form):
    login = CharField(max_length=30, widget=TextInput(attrs={
        'placeholder': 'Логин',
        'required': 'True',
        'class': 'textinput',
        'minlength': 6,
        'maxlength': 30,
        'pattern': '[A-Za-z0-9_]+',
    }))
    password = CharField(max_length=30, widget=PasswordInput(attrs={
        'placeholder': 'Пароль',
        'required': 'True',
        'class': 'textinput',
        'minlength': 6,
        'maxlength': 30,
        'pattern': '[A-Za-z0-9_]+',
    }))


class AddOrderForm(Form):
    checkindate = DateField(widget=DateInput(attrs={
        'required': 'True',
        'class': 'dateinput',
    }))
    checkoutdate = DateField(widget=DateInput(attrs={
        'required': 'True',
        'class': 'dateinput',
    }))
    numberofguests = IntegerField(min_value=1, max_value=4, widget=NumberInput(attrs={
        'placeholder': 'Количество проживающих',
        'required': 'True',
        'class': 'textinput addorder1_numberofguests_input'
    }))
    goback = BooleanField()