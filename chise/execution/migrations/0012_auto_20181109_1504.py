# Generated by Django 2.1.2 on 2018-11-09 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('execution', '0011_auto_20181108_2024'),
    ]

    operations = [
        migrations.AlterField(
            model_name='execution',
            name='modules',
            field=models.ManyToManyField(blank=True, to='core.Module', verbose_name='Modules'),
        ),
    ]
