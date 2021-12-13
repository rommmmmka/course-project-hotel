from django.contrib import admin
from .models import *


class VisitorAdmin(admin.ModelAdmin):
    list_display = ('visitorid', 'login', 'lastname', 'firstname', 'patronymic', 'citizenship')
    list_filter = (['citizenship'])


class OrderInfoAdmin(admin.ModelAdmin):
    list_display = ('orderid', 'visitorid', 'roomid', 'checkindate', 'checkoutdate', 'numberofguests', 'cost')
    list_filter = (['numberofguests'])


class FoodTypesAdmin(admin.ModelAdmin):
    list_display = ('foodtypeid', 'name', 'cost', 'avaliable', 'comment')
    list_filter = (['avaliable'])


class FoodAdmin(admin.ModelAdmin):
    list_display = ('foodid', 'orderid', 'foodtypeid')


class OrderStatusAdmin(admin.ModelAdmin):
    list_display = ('orderstatusid', 'orderid', 'orderactive', 'orderpayed')
    list_filter = ('orderactive', 'orderpayed')


class PaymentTypeAdmin(admin.ModelAdmin):
    list_display = ('paymenttypeid', 'name', 'avaliable')
    list_filter = (['avaliable'])


class RoomAdmin(admin.ModelAdmin):
    list_display = ('roomid', 'roomclassid', 'roomnumber', 'avaliable')
    list_filter = (['avaliable'])


class RoomClassAdmin(admin.ModelAdmin):
    list_display = ('roomclassid', 'name', 'cost', 'numberofpeople', 'comment')
    list_filter = (['numberofpeople'])


class AddServiceTypeAdmin(admin.ModelAdmin):
    list_display = ('addservicetypeid', 'name', 'cost', 'avaliable')
    list_filter = (['avaliable'])

class AddServicesAdmin(admin.ModelAdmin):
    list_display = ('addservicesid', 'orderid', 'addservicetypeid')


admin.site.register(Visitor, VisitorAdmin)
admin.site.register(Orderinfo, OrderInfoAdmin)
admin.site.register(Foodtype, FoodTypesAdmin)
admin.site.register(Food, FoodAdmin)
admin.site.register(Orderstatus, OrderStatusAdmin)
admin.site.register(Paymenttype, PaymentTypeAdmin)
admin.site.register(Room, RoomAdmin)
admin.site.register(Roomclass, RoomClassAdmin)
admin.site.register(Addservices, AddServicesAdmin)
admin.site.register(Addservicetype, AddServiceTypeAdmin)
