from django.shortcuts import render, redirect
from .models import *
from .forms import *
from .utils import *
import hashlib
from datetime import datetime, timedelta

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
    if not check_if_logged_in(request):
        return logout_action(request)
    if request.method == 'POST':
        print(request.POST)
        room = room_get(request.POST['checkindate'], request.POST['checkoutdate'], request.POST['roomclass'])
        days = (to_date(request.POST['checkoutdate']) - to_date(request.POST['checkindate'])).days + 1
        print(days)
        numberofguests = int(request.POST['numberofguests'])
        roomCost = int(Roomclass.objects.get(roomclassid=request.POST['roomclass']).cost)
        print(roomCost)
        foodCost = int(Foodtype.objects.get(foodtypeid=request.POST['foodtype']).cost)
        addServicesCost = 0;
        for el in request.POST['addservicetypes']:
            addServicesCost += int(Addservicetype.objects.get(addservicetypeid=el).cost)
        cost = roomCost * days + foodCost * days * numberofguests + addServicesCost * days

        orderinfo_obj = Orderinfo(
            checkindate=request.POST['checkindate'],
            checkoutdate=request.POST['checkoutdate'],
            numberofguests=numberofguests,
            cost=cost,
        )
        orderinfo_obj.visitorid_id = request.COOKIES.get('id')
        orderinfo_obj.roomid_id = room[0].roomid
        orderinfo_obj.save()
        orderstatus_obj = Orderstatus(
            orderid=orderinfo_obj,
            orderactive=True,
            orderpayed=False,
        )
        orderstatus_obj.paymenttypeid_id = request.POST['paymenttype']
        orderstatus_obj.save()
        food_obj = Food(orderid=orderinfo_obj)
        food_obj.foodtypeid_id = request.POST['foodtype']
        food_obj.save()
        for el in request.POST['addservicetypes']:
            addservices_obj = Addservices(orderid=orderinfo_obj)
            addservices_obj.addservicetypeid_id = el
            addservices_obj.save()
        return redirect_with_get(user_panel, {'addingorder_success': True})
    return redirect(user_panel)


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
    if not check_if_logged_in(request):
        return logout_action(request)
    form = AddOrderForm()
    if request.method == 'POST' and AddOrderForm(request.POST).is_valid():
        roomclass_list = roomclass_list_get(request.POST['checkindate'], request.POST['checkoutdate'], request.POST['numberofguests'])
        print(request.POST)
        return render(request, 'main/up_add_order2.html', {
            'form': form,
            'checkindate': request.POST['checkindate'],
            'checkoutdate': request.POST['checkoutdate'],
            'numberofguests': request.POST['numberofguests'],
            'roomclass_list': roomclass_list,
            'foodtype_list': Foodtype.objects.filter(avaliable=True),
            'addservicetype_list': Addservicetype.objects.filter(avaliable=True),
            'paymenttype_list': Paymenttype.objects.filter(avaliable=True),
        })
    return render(request, 'main/up_add_order1.html', {
        'form': form,
    })