# roomclass -> numberofpeople, comment
# foodtype -> comment
# room, foodtype, paymenttype, addservicetype -> avaliable
# visitor -> citizenship, passport
# room -> del hotelnumber
from django.db import models


class Visitor(models.Model):
    visitorid = models.AutoField(db_column='VisitorId', primary_key=True)  # Field name made lowercase.
    login = models.CharField(db_column='Login', max_length=30, blank=True, null=True)  # Field name made lowercase.
    passwordhash = models.CharField(db_column='PasswordHash', max_length=64, blank=True, null=True)  # Field name made lowercase.
    session = models.CharField(db_column='Session', max_length=32, blank=True, null=True)  # Field name made lowercase.
    lastname = models.CharField(db_column='Lastname', max_length=30, blank=True, null=True)  # Field name made lowercase.
    firstname = models.CharField(db_column='Firstname', max_length=30, blank=True, null=True)  # Field name made lowercase.
    patronymic = models.CharField(db_column='Patronymic', max_length=30, blank=True, null=True)  # Field name made lowercase.
    phonenumber = models.CharField(db_column='PhoneNumber', max_length=19, blank=True, null=True)  # Field name made lowercase.
    citizenship = models.CharField(db_column='Citizenship', max_length=30, blank=True, null=True)
    passport = models.CharField(db_column='Passport', max_length=15, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'visitor'


class Roomclass(models.Model):
    roomclassid = models.AutoField(db_column='RoomClassId', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=30, blank=True, null=True)  # Field name made lowercase.
    cost = models.PositiveIntegerField(db_column='Cost', blank=True, null=True)  # Field name made lowercase.
    numberofpeople = models.PositiveIntegerField(db_column='NumberOfPeople', blank=True, null=True)
    comment = models.CharField(db_column='Comment', max_length=200, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'roomclass'


class Room(models.Model):
    roomid = models.AutoField(db_column='RoomId', primary_key=True)  # Field name made lowercase.
    roomclassid = models.ForeignKey('Roomclass', models.DO_NOTHING, db_column='RoomClassId', blank=True, null=True)  # Field name made lowercase.
    roomnumber = models.PositiveIntegerField(db_column='RoomNumber', blank=True, null=True)  # Field name made lowercase.
    avaliable = models.IntegerField(db_column='Avaliable', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'room'


class Orderinfo(models.Model):
    orderid = models.AutoField(db_column='OrderId', primary_key=True)  # Field name made lowercase.
    visitorid = models.ForeignKey('Visitor', models.DO_NOTHING, db_column='VisitorId', blank=True, null=True)  # Field name made lowercase.
    roomid = models.ForeignKey('Room', models.DO_NOTHING, db_column='RoomId', blank=True, null=True)  # Field name made lowercase.
    checkindate = models.DateField(db_column='CheckInDate', blank=True, null=True)  # Field name made lowercase.
    checkoutdate = models.DateField(db_column='CheckOutDate', blank=True, null=True)  # Field name made lowercase.
    numberofguests = models.IntegerField(db_column='NumberOfGuests', blank=True, null=True)  # Field name made lowercase.
    cost = models.IntegerField(db_column='Cost', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'orderinfo'


class Foodtype(models.Model):
    foodtypeid = models.AutoField(db_column='FoodTypeId', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=30, blank=True, null=True)  # Field name made lowercase.
    cost = models.PositiveIntegerField(db_column='Cost', blank=True, null=True)  # Field name made lowercase.
    avaliable = models.IntegerField(db_column='Avaliable', blank=True, null=True)
    comment = models.CharField(db_column='Comment', max_length=200, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'foodtype'


class Food(models.Model):
    foodid = models.AutoField(db_column='FoodId', primary_key=True)  # Field name made lowercase.
    orderid = models.ForeignKey('Orderinfo', models.DO_NOTHING, db_column='OrderId', blank=True, null=True)  # Field name made lowercase.
    foodtypeid = models.ForeignKey('Foodtype', models.DO_NOTHING, db_column='FoodTypeId', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'food'


class Paymenttype(models.Model):
    paymenttypeid = models.AutoField(db_column='PaymentTypeId', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=30, blank=True, null=True)  # Field name made lowercase.
    avaliable = models.IntegerField(db_column='Avaliable', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'paymenttype'


class Orderstatus(models.Model):
    orderstatusid = models.AutoField(db_column='OrderStatusId', primary_key=True)  # Field name made lowercase.
    orderid = models.ForeignKey(Orderinfo, models.DO_NOTHING, db_column='OrderId', blank=True, null=True)  # Field name made lowercase.
    paymenttypeid = models.ForeignKey('Paymenttype', models.DO_NOTHING, db_column='PaymentTypeId', blank=True, null=True)  # Field name made lowercase.
    orderactive = models.IntegerField(db_column='OrderActive', blank=True, null=True)  # Field name made lowercase.
    orderpayed = models.IntegerField(db_column='OrderPayed', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'orderstatus'


class Addservicetype(models.Model):
    addservicetypeid = models.AutoField(db_column='AddServiceTypeId', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=30, blank=True, null=True)  # Field name made lowercase.
    cost = models.PositiveIntegerField(db_column='Cost', blank=True, null=True)  # Field name made lowercase.
    avaliable = models.IntegerField(db_column='Avaliable', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'addservicetype'


class Addservices(models.Model):
    addservicesid = models.AutoField(db_column='AddServicesId', primary_key=True)  # Field name made lowercase.
    orderid = models.ForeignKey('Orderinfo', models.DO_NOTHING, db_column='OrderId', blank=True, null=True)  # Field name made lowercase.
    addservicetypeid = models.ForeignKey('Addservicetype', models.DO_NOTHING, db_column='AddServiceTypeId', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'addservices'


class Employee(models.Model):
    employeeid = models.AutoField(db_column='EmployeeId', primary_key=True)  # Field name made lowercase.
    login = models.CharField(db_column='Login', max_length=30, blank=True, null=True)  # Field name made lowercase.
    passwordhash = models.CharField(db_column='PasswordHash', max_length=64, blank=True, null=True)  # Field name made lowercase.
    session = models.CharField(db_column='Session', max_length=32, blank=True, null=True)  # Field name made lowercase.
    lastname = models.CharField(db_column='Lastname', max_length=30, blank=True, null=True)  # Field name made lowercase.
    firstname = models.CharField(db_column='Firstname', max_length=30, blank=True, null=True)  # Field name made lowercase.
    patronymic = models.CharField(db_column='Patronymic', max_length=30, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'employee'
