# Generated by Django 3.1.3 on 2020-12-07 03:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0003_waitlist'),
    ]

    operations = [
        migrations.DeleteModel(
            name='WaitList',
        ),
    ]
