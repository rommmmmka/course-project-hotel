from django.shortcuts import render
from .utils import *
from .forms import *
from datetime import datetime


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
    response.delete_cookie('order_by')
    return response


def addorder_action(request):
    if not check_if_logged_in(request):
        return logout_action(request)
    if request.method == 'POST':
        room = room_get(request.POST['checkindate'], request.POST['checkoutdate'], request.POST['roomclass'])
        days = (to_date(request.POST['checkoutdate']) - to_date(request.POST['checkindate'])).days
        numberofguests = int(request.POST['numberofguests'])
        roomCost = int(Roomclass.objects.get(roomclassid=request.POST['roomclass']).cost)
        foodCost = 0
        if request.POST['foodtype'] != '0':
            foodCost = int(Foodtype.objects.get(foodtypeid=request.POST['foodtype']).cost)
        addServicesCost = 0
        if 'addservicetypes' in request.POST.keys():
            for el in request.POST.getlist('addservicetypes'):
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
        if request.POST['foodtype'] == '0':
            food_obj.included = False
        else:
            food_obj.included = True
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
    if Orderstatus.objects.filter(orderid=request.GET['orderid']).count() == 1:
        orderstatus_obj = Orderstatus.objects.get(orderid=request.GET['orderid'])
        orderstatus_obj.orderactive = False
        orderstatus_obj.save()
        return redirect_with_get(user_panel, {'removingorder_success': True, 'select_orderid': request.GET['orderid']})
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
        foodcost = 0
        food = Food.objects.get(orderid=orderid)
        if request.POST['foodtype'] == '0':
            food.foodtypeid_id = None
            food.included = False
        else:
            food.foodtypeid_id = request.POST['foodtype']
            food.included = True
            foodcost = Foodtype.objects.get(foodtypeid=request.POST['foodtype']).cost
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
            return redirect_with_get('user_panel', {'editingpassword_success': True})
        return redirect_with_get('up_edit_password', {'wrongpassword_error': True})
    return redirect('up_edit_password')


def editpersonalinfo_action(request):
    if not check_if_logged_in(request):
        return logout_action(request)
    if request.method == 'POST':
        visitor = Visitor.objects.get(visitorid=request.COOKIES.get('id'))
        visitor.lastname = request.POST['lastname']
        visitor.firstname = request.POST['firstname']
        visitor.patronymic = request.POST['patronymic']
        visitor.citizenship = request.POST['citizenship']
        visitor.passport = request.POST['passport']
        visitor.phonenumber = request.POST['phonenumber']
        visitor.save()
    return redirect_with_get('user_panel', {'editingpersonalinfo_success': True})

def changeorderby_action(request):
    if not check_if_logged_in(request):
        return logout_action(request)
    response = redirect('user_panel')
    if request.COOKIES.get('order_by') is None:
        response.set_cookie('order_by', 1, max_age=3600)
    else:
        response.delete_cookie('order_by')
    return response


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
    orders = Orderinfo.objects.raw("CALL get_orders(%s, %s);", [request.COOKIES.get('id'), 1 if request.COOKIES.get('order_by') is None else 2])
    orderid = request.GET.get('select_orderid')
    ordertype = ''
    if orderid is not None:
        ordertype = 'active' if Orderstatus.objects.get(orderid=orderid).orderactive == 1 else 'nonactive'
    return render(request, 'main/user_panel.html', {
        'orders': orders,
        'orders_exist': True if len(orders) != 0 else False,
        'personal_info': Visitor.objects.get(visitorid=request.COOKIES.get('id')),
        'currdate': datetime.now().date(),
        'select_orderid': 0 if orderid is None else int(orderid),
        'select_ordertype': ordertype,
        'order_by': 1 if request.COOKIES.get('order_by') == '1' else 2,
        'addingorder_success': request.GET.get('addingorder_success'),
        'removingorder_success': request.GET.get('removingorder_success'),
        'editingorder_success': request.GET.get('editingorder_success'),
        'editingpassword_success': request.GET.get('editingpassword_success'),
        'editingpersonalinfo_success': request.GET.get('editingpersonalinfo_success'),
    })


def up_add_order(request):
    if not check_if_logged_in(request):
        return logout_action(request)
    if request.method == 'POST':
        checkindate = request.POST['checkindate']
        checkoutdate = request.POST['checkoutdate']
        if request.POST['goback'] == 'True':
            return render(request, 'main/up_add_order1.html', {
                'login': request.COOKIES.get('login'),
                'goback': True,
                'error_no_empty_rooms': False,
                'checkindate': checkindate,
                'checkoutdate': checkoutdate,
                'numberofguests': request.POST['numberofguests'],
            })
        roomclass_list = roomclass_list_get(checkindate, checkoutdate, request.POST['numberofguests'])
        if len(roomclass_list) == 0:
            return render(request, 'main/up_add_order1.html', {
                'login': request.COOKIES.get('login'),
                'goback': True,
                'error_no_empty_rooms': True,
                'checkindate': checkindate,
                'checkoutdate': checkoutdate,
                'numberofguests': request.POST['numberofguests'],
            })
        return render(request, 'main/up_add_order2.html', {
            'login': request.COOKIES.get('login'),
            'checkindate': checkindate,
            'checkoutdate': checkoutdate,
            'days': (to_date(checkoutdate) - to_date(checkindate)).days,
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
    if Orderinfo.objects.filter(orderid=orderid).count() == 1:
        orderinfo = Orderinfo.objects.get(orderid=orderid)
        if orderinfo.visitorid_id != int(request.COOKIES.get('id')) or Orderstatus.objects.get(
                orderid=orderinfo.orderid).orderactive == 0:
            return redirect('user_panel')
        checkindate = orderinfo.checkindate
        checkoutdate = orderinfo.checkoutdate
        numberofguests = orderinfo.numberofguests
        room = Room.objects.filter(roomid=orderinfo.roomid_id).extra(select={
            'classname': 'SELECT name FROM roomclass WHERE roomclass.roomclassid = room.roomclassid',
            'classcost': 'SELECT cost FROM roomclass WHERE roomclass.roomclassid = room.roomclassid',
            'classcomment': 'SELECT comment FROM roomclass WHERE roomclass.roomclassid = room.roomclassid',
        }).get()
        foodtypeid_check = 0
        food_obj = Food.objects.get(orderid=orderid)
        if food_obj.included == 1:
            foodtypeid_check = food_obj.foodtypeid_id
        return render(request, 'main/up_edit_order.html', {
            'login': request.COOKIES.get('login'),
            'checkindate': str(checkindate),
            'checkoutdate': str(checkoutdate),
            'days': (checkoutdate - checkindate).days,
            'numberofguests': numberofguests,
            'room': room,
            'orderid': orderid,
            'foodtype_list': Foodtype.objects.filter(avaliable=True),
            'foodtypeid_check': foodtypeid_check,
            'addservicetype_list': Addservicetype.objects.filter(avaliable=True),
            'addservicetypeid_check': Addservices.objects.filter(orderid=orderid).values_list('addservicetypeid_id', flat=True),
            'paymenttype_list': Paymenttype.objects.filter(avaliable=True),
            'paymenttypeid_check': Orderstatus.objects.get(orderid=orderid).paymenttypeid_id,
        })
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
    personalinfo = Visitor.objects.get(visitorid=request.COOKIES.get('id'))
    citizenship_select = False
    if personalinfo.citizenship in ['Беларусь', 'Россия', 'Украина', 'Польша', 'Литва']:
        citizenship_select = True
    return render(request, 'main/up_edit_personal_info.html', {
        'login': request.COOKIES.get('login'),
        'personalinfo': personalinfo,
        'citizenship_select': citizenship_select,
    })
