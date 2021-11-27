# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Addservices(models.Model):
    orderid = models.PositiveIntegerField(db_column='OrderId', primary_key=True)  # Field name made lowercase.
    tv = models.IntegerField(db_column='TV', blank=True, null=True)  # Field name made lowercase.
    safedeposit = models.IntegerField(db_column='SafeDeposit', blank=True, null=True)  # Field name made lowercase.
    bar = models.IntegerField(db_column='Bar', blank=True, null=True)  # Field name made lowercase.


class Costs(models.Model):
    costsid = models.AutoField(db_column='CostsId', primary_key=True)  # Field name made lowercase.
    tablename = models.CharField(db_column='TableName', max_length=30, blank=True, null=True)  # Field name made lowercase.
    classname = models.CharField(db_column='ClassName', max_length=30, blank=True, null=True)  # Field name made lowercase.
    cost = models.PositiveIntegerField(blank=True, null=True)


class Employee(models.Model):
    employeeid = models.AutoField(db_column='EmployeeId', primary_key=True)  # Field name made lowercase.
    login = models.CharField(db_column='Login', max_length=30, blank=True, null=True)  # Field name made lowercase.
    passwordhash = models.CharField(db_column='PasswordHash', max_length=32, blank=True, null=True)  # Field name made lowercase.
    lastname = models.CharField(db_column='Lastname', max_length=30, blank=True, null=True)  # Field name made lowercase.
    firstname = models.CharField(db_column='Firstname', max_length=30, blank=True, null=True)  # Field name made lowercase.
    patronymic = models.CharField(db_column='Patronymic', max_length=30, blank=True, null=True)  # Field name made lowercase.


class Food(models.Model):
    orderid = models.PositiveIntegerField(db_column='OrderId', primary_key=True)  # Field name made lowercase.
    breakfast = models.IntegerField(db_column='Breakfast', blank=True, null=True)  # Field name made lowercase.
    lunch = models.IntegerField(db_column='Lunch', blank=True, null=True)  # Field name made lowercase.
    dinner = models.IntegerField(db_column='Dinner', blank=True, null=True)  # Field name made lowercase.


class Orderinfo(models.Model):
    orderid = models.AutoField(db_column='OrderId', primary_key=True)  # Field name made lowercase.
    visitorid = models.PositiveIntegerField(db_column='VisitorId', blank=True, null=True)  # Field name made lowercase.
    checkindate = models.DateField(db_column='CheckInDate', blank=True, null=True)  # Field name made lowercase.
    checkoutdate = models.DateField(db_column='CheckOutDate', blank=True, null=True)  # Field name made lowercase.
    numberofguests = models.IntegerField(db_column='NumberOfGuests', blank=True, null=True)  # Field name made lowercase.
    cost = models.IntegerField(db_column='Cost', blank=True, null=True)  # Field name made lowercase.


class Orderstatus(models.Model):
    orderid = models.PositiveIntegerField(db_column='OrderId', primary_key=True)  # Field name made lowercase.
    orderactive = models.IntegerField(db_column='OrderActive', blank=True, null=True)  # Field name made lowercase.


class Paymentstatus(models.Model):
    orderid = models.PositiveIntegerField(db_column='OrderId', primary_key=True)  # Field name made lowercase.
    ispayed = models.IntegerField(db_column='IsPayed', blank=True, null=True)  # Field name made lowercase.


class Room(models.Model):
    roomid = models.AutoField(db_column='RoomId', primary_key=True)  # Field name made lowercase.
    orderid = models.PositiveIntegerField(db_column='OrderId', blank=True, null=True)  # Field name made lowercase.
    hotelnumber = models.PositiveIntegerField(db_column='HotelNumber', blank=True, null=True)  # Field name made lowercase.
    roomnumber = models.PositiveIntegerField(db_column='RoomNumber', blank=True, null=True)  # Field name made lowercase.


class Roomclass(models.Model):
    roomid = models.PositiveIntegerField(db_column='RoomId', primary_key=True)  # Field name made lowercase.
    standart = models.IntegerField(db_column='Standart', blank=True, null=True)  # Field name made lowercase.
    premium = models.IntegerField(db_column='Premium', blank=True, null=True)  # Field name made lowercase.
    deluxe = models.IntegerField(db_column='Deluxe', blank=True, null=True)  # Field name made lowercase.


class Visitor(models.Model):
    visitorid = models.AutoField(db_column='VisitorId', primary_key=True)  # Field name made lowercase.
    login = models.CharField(db_column='Login', max_length=30, blank=True, null=True)  # Field name made lowercase.
    passwordhash = models.CharField(db_column='PasswordHash', max_length=64, blank=True, null=True)  # Field name made lowercase.
    session = models.CharField(db_column='Session', max_length=32, blank=True, null=True)  # Field name made lowercase.
    lastname = models.CharField(db_column='Lastname', max_length=30, blank=True, null=True)  # Field name made lowercase.
    firstname = models.CharField(db_column='Firstname', max_length=30, blank=True, null=True)  # Field name made lowercase.
    patronymic = models.CharField(db_column='Patronymic', max_length=30, blank=True, null=True)  # Field name made lowercase.
    phonenumber = models.CharField(db_column='PhoneNumber', max_length=15, blank=True, null=True)  # Field name made lowercase.
