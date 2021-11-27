from django.shortcuts import render, redirect
from .models import *
from .forms import *
from .utils import *
import hashlib

"""
TODO
Случайная соль для каждого пользователя
Хранение в БД времени жизни куки
Перетащить некоторые функции в модели
Реализовать смену пароля


"""


def register_action(request):
    if request.method == 'POST' and RegisterForm(request.POST).is_valid():
        registrationData = request.POST.copy()
        # loginRepeats = True if len(list(Visitor.objects.raw(f"SELECT * FROM main_visitor WHERE Login = '{registrationData.__getitem__('login')}'"))) == 1 else False
        if check_if_login_repeats(registrationData['login']):
            return redirect_with_get('register', {'register_error': True})
        passwordHashed = str(hashlib.sha256(
            str(registrationData['login'] + registrationData['passwordhash'] + '4lmAIQg0eRvU').encode(
                'utf-8')).hexdigest())  # random salt
        registrationData['passwordhash'] = passwordHashed
        RegisterForm(registrationData).save()
        return redirect_with_get('index', {'register_success': True})
    return redirect('index')


def login_action(request):
    if request.method == 'POST' and LoginForm(request.POST).is_valid():
        login = request.POST['login']
        passwordHashed = str(hashlib.sha256(
            str(login + request.POST['password'] + '4lmAIQg0eRvU').encode('utf-8')).hexdigest())  # random salt
        if check_if_login_repeats(login) and Visitor.objects.get(login=login).passwordhash == passwordHashed:
            session = salt_generator(32)
            obj = Visitor.objects.get(login=login)
            obj.session = session
            id = obj.visitorid
            obj.save()
            response = redirect('user_panel')
            response.set_cookie('id', id, max_age=3600)
            response.set_cookie('session', session, max_age=3600)
            return response
        else:
            return redirect_with_get(index, {'login_error': True})

    return redirect('index')


def logout_action(request):
    response = redirect('index')
    response.delete_cookie('id')
    response.delete_cookie('session')
    return response


def addorder_action(request):
    return 0


def index(request):
    form = LoginForm()
    return render(request, 'main/index.html', {
        'form': form,
        'register_success': request.GET.get('register_success'),
        'login_error': request.GET.get('login_error'),
    })


def register(request):
    form = RegisterForm()
    return render(request, 'main/register.html', {
        'form': form,
        'register_error': request.GET.get('register_error'),
    })


def user_panel(request):
    if not check_if_logged_in(request):
        return logout_action(request)
    orders = Orderinfo.objects.filter(visitorid=request.COOKIES.get('id'))
    return render(request, 'main/user_panel.html', {
        'orders': orders,
    })


def up_change_password(request):
    if not check_if_logged_in(request):
        return logout_action(request)
    return render(request, 'main/up_change_password.html')

def up_add_order(request):
    """
    1:
    Даты заселения, выселения, количество человек
    Реализовать поиск свободного номера
    Тип питания
    Выбор доп услуг
    """
    if not check_if_logged_in(request):
        return logout_action(request)
    form = AddOrderForm()
    if request.method == 'POST' and AddOrderForm(request.POST).is_valid():
        roomclass_list = roomclass_list_get(request.POST['checkindate'], request.POST['checkoutdate'], request.POST['numberofguests'])
        return render(request, 'main/up_add_order2.html', {
            'form': form,
            'prevpage_data': request.POST,
            'roomclass_list': roomclass_list,
            'foodtype_list': Foodtype.objects.filter(avaliable=True),
            'addservicetype_list': Addservicetype.objects.filter(avaliable=True),
        })
    return render(request, 'main/up_add_order1.html', {
        'form': form,
    })