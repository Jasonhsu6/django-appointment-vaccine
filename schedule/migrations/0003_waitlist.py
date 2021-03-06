# Generated by Django 3.1.3 on 2020-12-04 03:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0002_auto_20201124_2128'),
    ]

    operations = [
        migrations.CreateModel(
            name='WaitList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('joined', models.DateTimeField(auto_now=True, verbose_name='created at')),
                ('first_name', models.CharField(max_length=20)),
                ('last_name', models.CharField(max_length=20)),
                ('email', models.EmailField(blank=True, max_length=100)),
                ('phone', models.CharField(max_length=14)),
                ('birthday', models.DateField(verbose_name='birthday')),
                ('picked', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'wait list',
                'ordering': ['joined', 'picked'],
            },
        ),
    ]
