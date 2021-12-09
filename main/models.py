# roomclass -> numberofpeople, comment
# foodtype -> comment
# room, foodtype, paymenttype, addservicetype -> avaliable
# visitor -> citizenship, passport
# room -> del hotelnumber
from django.db import models


class Visitor(models.Model):
    visitorid = models.AutoField(db_column='VisitorId', primary_key=True, verbose_name='№')
    login = models.CharField(db_column='Login', max_length=30, blank=True, null=True, verbose_name='Логин')
    passwordhash = models.CharField(db_column='PasswordHash', max_length=64, blank=True, null=True, verbose_name='Хеш пароля')
    session = models.CharField(db_column='Session', max_length=32, blank=True, null=True, verbose_name='ID сессии')
    lastname = models.CharField(db_column='Lastname', max_length=30, blank=True, null=True, verbose_name='Фамилия')
    firstname = models.CharField(db_column='Firstname', max_length=30, blank=True, null=True, verbose_name='Имя')
    patronymic = models.CharField(db_column='Patronymic', max_length=30, blank=True, null=True, verbose_name='Отчество')
    phonenumber = models.CharField(db_column='PhoneNumber', max_length=19, blank=True, null=True, verbose_name='Номер телефона')
    citizenship = models.CharField(db_column='Citizenship', max_length=30, blank=True, null=True, verbose_name='Гражданство')
    passport = models.CharField(db_column='Passport', max_length=15, blank=True, null=True, verbose_name='Серия и номер паспорта')

    class Meta:
        managed = True
        db_table = 'visitor'
        verbose_name = 'Посетитель'
        verbose_name_plural = 'Посетители'

    def __str__(self):
        return self.login


class Roomclass(models.Model):
    roomclassid = models.AutoField(db_column='RoomClassId', primary_key=True, verbose_name='№')
    name = models.CharField(db_column='Name', max_length=30, blank=True, null=True, verbose_name='Название класса')
    cost = models.PositiveIntegerField(db_column='Cost', blank=True, null=True, verbose_name='Стоимость')
    numberofpeople = models.PositiveIntegerField(db_column='NumberOfPeople', blank=True, null=True, verbose_name='Вместимость')
    comment = models.CharField(db_column='Comment', max_length=200, blank=True, null=True, verbose_name='Описание')

    class Meta:
        managed = True
        db_table = 'roomclass'
        verbose_name = 'Класс номера'
        verbose_name_plural = 'Классы номеров'

    def __str__(self):
        return self.name


class Room(models.Model):
    roomid = models.AutoField(db_column='RoomId', primary_key=True, verbose_name='№')
    roomclassid = models.ForeignKey('Roomclass', models.DO_NOTHING, db_column='RoomClassId', blank=True, null=True, verbose_name='Класс номера')
    roomnumber = models.PositiveIntegerField(db_column='RoomNumber', blank=True, null=True, verbose_name='Номер комнаты')
    avaliable = models.IntegerField(db_column='Avaliable', blank=True, null=True, verbose_name='Активный')

    class Meta:
        managed = True
        db_table = 'room'
        verbose_name = 'Номер'
        verbose_name_plural = 'Номера'

    def __str__(self):
        return f"{self.roomnumber} ({self.roomclassid})"


class Orderinfo(models.Model):
    orderid = models.AutoField(db_column='OrderId', primary_key=True, verbose_name='№')
    visitorid = models.ForeignKey('Visitor', models.DO_NOTHING, db_column='VisitorId', blank=True, null=True, verbose_name='Посетитель')
    roomid = models.ForeignKey('Room', models.DO_NOTHING, db_column='RoomId', blank=True, null=True, verbose_name='Комната')
    checkindate = models.DateField(db_column='CheckInDate', blank=True, null=True, verbose_name='Дата заселения')
    checkoutdate = models.DateField(db_column='CheckOutDate', blank=True, null=True, verbose_name='Дата выселения')
    numberofguests = models.IntegerField(db_column='NumberOfGuests', blank=True, null=True, verbose_name='Количество гостей')
    cost = models.IntegerField(db_column='Cost', blank=True, null=True, verbose_name='Стоимость')

    class Meta:
        managed = True
        db_table = 'orderinfo'
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f"Заказ №{self.orderid}"


class Foodtype(models.Model):
    foodtypeid = models.AutoField(db_column='FoodTypeId', primary_key=True, verbose_name='№')
    name = models.CharField(db_column='Name', max_length=30, blank=True, null=True, verbose_name='Название')
    cost = models.PositiveIntegerField(db_column='Cost', blank=True, null=True, verbose_name='Стоимость')
    avaliable = models.IntegerField(db_column='Avaliable', blank=True, null=True, verbose_name='Активный')
    comment = models.CharField(db_column='Comment', max_length=200, blank=True, null=True, verbose_name='Описание')

    class Meta:
        managed = True
        db_table = 'foodtype'
        verbose_name = 'Тип питания'
        verbose_name_plural = 'Типы питания'

    def __str__(self):
        return self.name


class Food(models.Model):
    foodid = models.AutoField(db_column='FoodId', primary_key=True, verbose_name='№')
    orderid = models.ForeignKey('Orderinfo', models.DO_NOTHING, db_column='OrderId', blank=True, null=True, verbose_name='Заказ')
    foodtypeid = models.ForeignKey('Foodtype', models.DO_NOTHING, db_column='FoodTypeId', blank=True, null=True, verbose_name='Тип питания')

    class Meta:
        managed = True
        db_table = 'food'
        verbose_name = 'Питание'
        verbose_name_plural = 'Питание'


class Paymenttype(models.Model):
    paymenttypeid = models.AutoField(db_column='PaymentTypeId', primary_key=True, verbose_name='№')
    name = models.CharField(db_column='Name', max_length=30, blank=True, null=True, verbose_name='Название')
    avaliable = models.IntegerField(db_column='Avaliable', blank=True, null=True, verbose_name='Активный')

    class Meta:
        managed = True
        db_table = 'paymenttype'
        verbose_name = 'Тип оплаты'
        verbose_name_plural = 'Типы оплаты'

    def __str__(self):
        return self.name


class Orderstatus(models.Model):
    orderstatusid = models.AutoField(db_column='OrderStatusId', primary_key=True, verbose_name='№')
    orderid = models.ForeignKey(Orderinfo, models.DO_NOTHING, db_column='OrderId', blank=True, null=True, verbose_name='Заказ')
    paymenttypeid = models.ForeignKey('Paymenttype', models.DO_NOTHING, db_column='PaymentTypeId', blank=True, null=True, verbose_name='Тип оплаты')
    orderactive = models.IntegerField(db_column='OrderActive', blank=True, null=True, verbose_name='Активный')
    orderpayed = models.IntegerField(db_column='OrderPayed', blank=True, null=True, verbose_name='Оплаченный')

    class Meta:
        managed = True
        db_table = 'orderstatus'
        verbose_name = 'Статус заказа'
        verbose_name_plural = 'Статусы заказов'

    def __str__(self):
        return f"Статус заказа №{self.orderid}"


class Addservicetype(models.Model):
    addservicetypeid = models.AutoField(db_column='AddServiceTypeId', primary_key=True, verbose_name='№')
    name = models.CharField(db_column='Name', max_length=30, blank=True, null=True, verbose_name='Название')
    cost = models.PositiveIntegerField(db_column='Cost', blank=True, null=True, verbose_name='Стоимость')
    avaliable = models.IntegerField(db_column='Avaliable', blank=True, null=True, verbose_name='Активный')

    class Meta:
        managed = True
        db_table = 'addservicetype'
        verbose_name = 'Тип доп. услуги'
        verbose_name_plural = 'Типы доп. услуг'

    def __str__(self):
        return self.name


class Addservices(models.Model):
    addservicesid = models.AutoField(db_column='AddServicesId', primary_key=True, verbose_name='№')
    orderid = models.ForeignKey('Orderinfo', models.DO_NOTHING, db_column='OrderId', blank=True, null=True, verbose_name='Заказ')
    addservicetypeid = models.ForeignKey('Addservicetype', models.DO_NOTHING, db_column='AddServiceTypeId', blank=True, null=True, verbose_name='Тип доп. услуги')

    class Meta:
        managed = True
        db_table = 'addservices'
        verbose_name = 'Доп. услуга'
        verbose_name_plural = 'Доп. услуги'
