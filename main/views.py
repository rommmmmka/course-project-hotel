from django.db.models import Subquery, OuterRef
from django.shortcuts import render, redirect
from .models import *
from .forms import *
from .utils import *
from datetime import datetime, timedelta
from django.db import connection

"""
TODO
Случайная соль для каждого пользователя
Хранение в БД времени жизни куки
Перетащить некоторые функции в модели
Реализовать смену пароля
Вывод номера заказа и номера комнаты


"""


def register_action(request):
    if request.method == 'POST':
        registrationData = request.POST.copy()
        if check_if_login_repeats(registrationData['login']):
            return redirect_with_get('register', {'register_error': True})
        passwordHashed = hash(registrationData['login'] + registrationData['passwordhash'])
        registrationData['passwordhash'] = passwordHashed
        RegisterForm(registrationData).save()
        return redirect_with_get('index', {'register_success': True})
    return redirect('index')


def login_action(request):
    if request.method == 'POST':
        login = request.POST['login']
        passwordHashed = hash(login + request.POST['password'])
        if check_if_login_repeats(login) and Visitor.objects.get(login=login).passwordhash == passwordHashed:
            session = salt_generator(32)
            obj = Visitor.objects.get(login=login)
            obj.session = session
            id = obj.visitorid
            obj.save()
            response = redirect('user_panel')
            response.set_cookie('id', id, max_age=3600)
            response.set_cookie('login', login, max_age=3600)
            response.set_cookie('session', session, max_age=3600)
            return response
        else:
            return redirect_with_get(index, {'login_error': True})
    return redirect('index')


def logout_action(request):
    response = redirect_with_get('index', {'logout_action': True})
    response.delete_cookie('id')
    response.delete_cookie('session')
    response.delete_cookie('login')
    return response


def addorder_action(request):
    if not check_if_logged_in(request):
        return logout_action(request)
    if request.method == 'POST':
        room = room_get(request.POST['checkindate'], request.POST['checkoutdate'], request.POST['roomclass'])
        days = (to_date(request.POST['checkoutdate']) - to_date(request.POST['checkindate'])).days
        numberofguests = int(request.POST['numberofguests'])
        roomCost = int(Roomclass.objects.get(roomclassid=request.POST['roomclass']).cost)
        foodCost = int(Foodtype.objects.get(foodtypeid=request.POST['foodtype']).cost)
        addServicesCost = 0
        if 'addservicetypes' in request.POST.keys():
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
        orderid = orderinfo_obj.orderid
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
        if 'addservicetypes' in request.POST.keys():
            for el in request.POST.getlist('addservicetypes'):
                addservices_obj = Addservices(orderid=orderinfo_obj)
                addservices_obj.addservicetypeid_id = el
                addservices_obj.save()
        return redirect_with_get(user_panel, {'addingorder_success': True, 'select_orderid': orderid})
    return redirect(user_panel)


def rmorder_action(request):
    if not check_if_logged_in(request):
        return logout_action(request)
    try:
        orderstatus_obj = Orderstatus.objects.get(orderid=request.GET['orderid'])
        orderstatus_obj.orderactive = False
        orderstatus_obj.save()
        return redirect_with_get(user_panel, {'removingorder_success': True, 'select_orderid': request.GET['orderid']})
    except:
        return redirect(user_panel)


def editorder_action(request):
    if not check_if_logged_in(request):
        return logout_action(request)
    if request.method == 'POST':
        orderid = request.POST['orderid']
        order = Orderinfo.objects.get(orderid=orderid)
        days = (order.checkoutdate - order.checkindate).days
        numberofguests = order.numberofguests
        roomclassid = Room.objects.get(roomid=order.roomid_id).roomclassid_id
        roomcost = Roomclass.objects.get(roomclassid=roomclassid).cost
        foodcost = Foodtype.objects.get(foodtypeid=request.POST['foodtype']).cost
        food = Food.objects.get(orderid=orderid)
        food.foodtypeid_id = request.POST['foodtype']
        food.save()
        addservicescost = 0
        if 'addservicetypes' in request.POST.keys():
            for el in request.POST.getlist('addservicetypes'):
                addservicescost += int(Addservicetype.objects.get(addservicetypeid=el).cost)
                addservices_obj = Addservices()
                addservices_obj.orderid_id = orderid
                addservices_obj.addservicetypeid_id = el
                addservices_obj.save()
        cost = roomcost * days + foodcost * days * numberofguests + addservicescost * days
        order.cost = cost
        order.save()
        orderstatus = Orderstatus.objects.get(orderid=orderid)
        orderstatus.paymenttypeid_id = request.POST['paymenttype']
        orderstatus.save()
        return redirect_with_get(user_panel, {'editingorder_success': True, 'select_orderid': request.POST['orderid']})
    return redirect(user_panel)


def editpassword_action(request):
    if not check_if_logged_in(request):
        return logout_action(request)
    login = request.COOKIES.get('login')
    oldpass = hash(login + request.POST['password_old'])
    if check_if_login_repeats(login):
        visitor = Visitor.objects.get(login=login)
        if visitor.passwordhash == oldpass:
            newpass = hash(login + request.POST['password_new'])
            visitor.passwordhash = newpass
            visitor.save()
            print('1111')
            return redirect_with_get('user_panel', {'editingpassword_success': True})
        return redirect_with_get('up_edit_password', {'wrongpassword_error': True})
    return redirect('up_edit_password')


def index(request):
    form = LoginForm()
    return render(request, 'main/index.html', {
        'form': form,
        'register_success': request.GET.get('register_success'),
        'login_error': request.GET.get('login_error'),
        'logout_action': request.GET.get('logout_action'),
        'play_login_anim': request.GET.get('play_login_anim'),
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
    orders = Orderinfo.objects.extra(select={
        "active": "SELECT orderactive FROM orderstatus WHERE orderstatus.OrderId = orderinfo.OrderId",
        "payed": "SELECT orderpayed FROM orderstatus WHERE orderstatus.OrderId = orderinfo.OrderId",
        "paymentname": "SELECT name FROM paymenttype WHERE paymenttype.PaymentTypeId = (SELECT PaymentTypeId FROM orderstatus WHERE orderstatus.OrderId = orderinfo.OrderId)"
    }).order_by('-checkindate')
    orderid = request.GET.get('select_orderid')
    ordertype = ''
    if orderid != None:
        ordertype = 'active' if Orderstatus.objects.get(orderid=orderid).orderactive == 1 else 'nonactive'
    print(request.GET.get('editingpassword_success'))
    return render(request, 'main/user_panel.html', {
        'orders': orders,
        'personal_info': Visitor.objects.get(visitorid=request.COOKIES.get('id')),
        'currdate': datetime.now().date(),
        'select_orderid': 0 if orderid == None else int(orderid),
        'select_ordertype': ordertype,
        'addingorder_success': request.GET.get('addingorder_success'),
        'removingorder_success': request.GET.get('removingorder_success'),
        'editingorder_success': request.GET.get('editingorder_success'),
        'editingpassword_success': request.GET.get('editingpassword_success'),
    })


def up_add_order(request):
    if not check_if_logged_in(request):
        return logout_action(request)
    if request.method == 'POST':
        if request.POST['goback'] == 'True':
            return render(request, 'main/up_add_order1.html', {
                'login': request.COOKIES.get('login'),
                'goback': True,
                'error_no_empty_rooms': False,
                'checkindate': request.POST['checkindate'],
                'checkoutdate': request.POST['checkoutdate'],
                'numberofguests': request.POST['numberofguests'],
            })
        roomclass_list = roomclass_list_get(request.POST['checkindate'], request.POST['checkoutdate'],
                                            request.POST['numberofguests'])
        if len(roomclass_list) == 0:
            return render(request, 'main/up_add_order1.html', {
                'login': request.COOKIES.get('login'),
                'goback': True,
                'error_no_empty_rooms': True,
                'checkindate': request.POST['checkindate'],
                'checkoutdate': request.POST['checkoutdate'],
                'numberofguests': request.POST['numberofguests'],
            })
        return render(request, 'main/up_add_order2.html', {
            'login': request.COOKIES.get('login'),
            'checkindate': request.POST['checkindate'],
            'checkoutdate': request.POST['checkoutdate'],
            'numberofguests': request.POST['numberofguests'],
            'roomclass_list': roomclass_list,
            'foodtype_list': Foodtype.objects.filter(avaliable=True),
            'addservicetype_list': Addservicetype.objects.filter(avaliable=True),
            'paymenttype_list': Paymenttype.objects.filter(avaliable=True),
        })
    return render(request, 'main/up_add_order1.html', {
        'login': request.COOKIES.get('login'),
        'goback': False,
        'error_no_empty_rooms': False,
    })


def up_edit_order(request):
    if not check_if_logged_in(request):
        return logout_action(request)
    orderid = request.GET.get('orderid')
    try:
        orderinfo = Orderinfo.objects.get(orderid=orderid)
        if orderinfo.visitorid_id != int(request.COOKIES.get('id')) or Orderstatus.objects.get(
                orderid=orderinfo.orderid).orderactive == 0:
            return redirect('user_panel')
        checkindate = orderinfo.checkindate
        checkoutdate = orderinfo.checkoutdate
        numberofguests = orderinfo.numberofguests
        days = (checkoutdate - checkindate).days
        room = Room.objects.filter(roomid=orderinfo.roomid_id).extra(select={
            'classname': 'SELECT name FROM roomclass WHERE roomclass.roomclassid = room.roomclassid',
            'classcost': 'SELECT cost FROM roomclass WHERE roomclass.roomclassid = room.roomclassid',
            'classcomment': 'SELECT comment FROM roomclass WHERE roomclass.roomclassid = room.roomclassid',
        }).get()
        return render(request, 'main/up_edit_order.html', {
            'login': request.COOKIES.get('login'),
            'checkindate': str(checkindate),
            'checkoutdate': str(checkoutdate),
            'numberofguests': numberofguests,
            'room': room,
            'orderid': orderid,
            'foodtype_list': Foodtype.objects.filter(avaliable=True),
            'foodtypeid_check': Food.objects.get(orderid=orderid).foodtypeid_id,
            'addservicetype_list': Addservicetype.objects.filter(avaliable=True),
            'addservicetypeid_check': Addservices.objects.filter(orderid=orderid).values_list('addservicetypeid_id',
                                                                                              flat=True),
            'paymenttype_list': Paymenttype.objects.filter(avaliable=True),
            'paymenttypeid_check': Orderstatus.objects.get(orderid=orderid).paymenttypeid_id,
        })
    except:
        return redirect('user_panel')


def up_edit_password(request):
    if not check_if_logged_in(request):
        return logout_action(request)
    return render(request, 'main/up_edit_password.html', {
        'login': request.COOKIES.get('login'),
        'wrongpassword_error': request.GET.get('wrongpassword_error'),
    })


def up_edit_personal_info(request):
    if not check_if_logged_in(request):
        return logout_action(request)
    return 0
