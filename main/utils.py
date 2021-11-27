import random
from django.urls import reverse
from urllib.parse import urlencode
from django.shortcuts import redirect
from .models import *


def salt_generator(length):
    alphabet = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    str = ''
    for i in range(length):
        str += random.choice(alphabet)
    return str


def redirect_with_get(url, query):
    base_url = reverse(url)
    query_string = urlencode(query)
    url = '{}?{}'.format(base_url, query_string)
    return redirect(url)


def check_if_login_repeats(login):
    return True if Visitor.objects.filter(login=login).count() == 1 else False #сделать по-человечески


def check_if_logged_in(request):
    obj = Visitor.objects.filter(visitorid=request.COOKIES.get('id'))
    if obj.count() == 0 or obj[0].session != request.COOKIES.get('session'):
        return False
    return True


def roomclass_list_get(checkindate, checkoutdate, numberofguests):
    roomclass_list = Roomclass.objects.raw("CALL get_roomclasses(%s, %s, %s);", [checkindate, checkoutdate, numberofguests])
    return roomclass_list


def room_get(checkindate, checkoutdate, roomclassid):
    room = Room.objects.raw("CALL get_room(%s, %s, %);", [checkindate, checkoutdate, roomclassid])
    print(room)
    for el in room:
        print(el)
    return room
