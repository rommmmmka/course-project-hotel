# Generated by Django 3.2.9 on 2021-12-11 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_auto_20211211_1722'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visitor',
            name='visitorid',
            field=models.IntegerField(db_column='VisitorId', primary_key=True, serialize=False, verbose_name='№'),
        ),
    ]
