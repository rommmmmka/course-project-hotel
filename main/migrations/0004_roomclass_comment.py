# Generated by Django 3.2.9 on 2021-11-27 04:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20211127_0001'),
    ]

    operations = [
        migrations.AddField(
            model_name='roomclass',
            name='comment',
            field=models.CharField(blank=True, db_column='Comment', max_length=200, null=True),
        ),
    ]
