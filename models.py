# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Addservices(models.Model):
    addservicesid = models.AutoField(db_column='AddServicesId', primary_key=True)  # Field name made lowercase.
    orderid = models.ForeignKey('Orderinfo', models.DO_NOTHING, db_column='OrderId', blank=True, null=True)  # Field name made lowercase.
    addservicetypeid = models.ForeignKey('Addservicetype', models.DO_NOTHING, db_column='AddServiceTypeId', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'addservices'


class Addservicetype(models.Model):
    addservicetypeid = models.AutoField(db_column='AddServiceTypeId', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=30, blank=True, null=True)  # Field name made lowercase.
    cost = models.PositiveIntegerField(db_column='Cost', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'addservicetype'


class Employee(models.Model):
    employeeid = models.AutoField(db_column='EmployeeId', primary_key=True)  # Field name made lowercase.
    login = models.CharField(db_column='Login', max_length=30, blank=True, null=True)  # Field name made lowercase.
    passwordhash = models.CharField(db_column='PasswordHash', max_length=64, blank=True, null=True)  # Field name made lowercase.
    session = models.CharField(db_column='Session', max_length=32, blank=True, null=True)  # Field name made lowercase.
    lastname = models.CharField(db_column='Lastname', max_length=30, blank=True, null=True)  # Field name made lowercase.
    firstname = models.CharField(db_column='Firstname', max_length=30, blank=True, null=True)  # Field name made lowercase.
    patronymic = models.CharField(db_column='Patronymic', max_length=30, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'employee'


class Food(models.Model):
    foodid = models.AutoField(db_column='FoodId', primary_key=True)  # Field name made lowercase.
    orderid = models.ForeignKey('Orderinfo', models.DO_NOTHING, db_column='OrderId', blank=True, null=True)  # Field name made lowercase.
    foodtypeid = models.ForeignKey('Foodtype', models.DO_NOTHING, db_column='FoodTypeId', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'food'


class Foodtype(models.Model):
    foodtypeid = models.AutoField(db_column='FoodTypeId', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=30, blank=True, null=True)  # Field name made lowercase.
    cost = models.PositiveIntegerField(db_column='Cost', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'foodtype'


class Orderinfo(models.Model):
    orderid = models.AutoField(db_column='OrderId', primary_key=True)  # Field name made lowercase.
    visitorid = models.ForeignKey('Visitor', models.DO_NOTHING, db_column='VisitorId', blank=True, null=True)  # Field name made lowercase.
    roomid = models.ForeignKey('Room', models.DO_NOTHING, db_column='RoomId', blank=True, null=True)  # Field name made lowercase.
    checkindate = models.DateField(db_column='CheckInDate', blank=True, null=True)  # Field name made lowercase.
    checkoutdate = models.DateField(db_column='CheckOutDate', blank=True, null=True)  # Field name made lowercase.
    numberofguests = models.IntegerField(db_column='NumberOfGuests', blank=True, null=True)  # Field name made lowercase.
    cost = models.IntegerField(db_column='Cost', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'orderinfo'


class Orderstatus(models.Model):
    orderstatusid = models.AutoField(db_column='OrderStatusId', primary_key=True)  # Field name made lowercase.
    orderid = models.ForeignKey(Orderinfo, models.DO_NOTHING, db_column='OrderId', blank=True, null=True)  # Field name made lowercase.
    paymenttypeid = models.ForeignKey('Paymenttype', models.DO_NOTHING, db_column='PaymentTypeId', blank=True, null=True)  # Field name made lowercase.
    orderactive = models.IntegerField(db_column='OrderActive', blank=True, null=True)  # Field name made lowercase.
    orderpayed = models.IntegerField(db_column='OrderPayed', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'orderstatus'


class Paymenttype(models.Model):
    paymenttypeid = models.AutoField(db_column='PaymentTypeId', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=30, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'paymenttype'


class Room(models.Model):
    roomid = models.AutoField(db_column='RoomId', primary_key=True)  # Field name made lowercase.
    roomclassid = models.ForeignKey('Roomclass', models.DO_NOTHING, db_column='RoomClassId', blank=True, null=True)  # Field name made lowercase.
    hotelnumber = models.PositiveIntegerField(db_column='HotelNumber', blank=True, null=True)  # Field name made lowercase.
    roomnumber = models.PositiveIntegerField(db_column='RoomNumber', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'room'


class Roomclass(models.Model):
    roomclassid = models.AutoField(db_column='RoomClassId', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=30, blank=True, null=True)  # Field name made lowercase.
    cost = models.PositiveIntegerField(db_column='Cost', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'roomclass'


class Visitor(models.Model):
    visitorid = models.AutoField(db_column='VisitorId', primary_key=True)  # Field name made lowercase.
    login = models.CharField(db_column='Login', max_length=30, blank=True, null=True)  # Field name made lowercase.
    passwordhash = models.CharField(db_column='PasswordHash', max_length=64, blank=True, null=True)  # Field name made lowercase.
    session = models.CharField(db_column='Session', max_length=32, blank=True, null=True)  # Field name made lowercase.
    lastname = models.CharField(db_column='Lastname', max_length=30, blank=True, null=True)  # Field name made lowercase.
    firstname = models.CharField(db_column='Firstname', max_length=30, blank=True, null=True)  # Field name made lowercase.
    patronymic = models.CharField(db_column='Patronymic', max_length=30, blank=True, null=True)  # Field name made lowercase.
    phonenumber = models.CharField(db_column='PhoneNumber', max_length=15, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'visitor'
