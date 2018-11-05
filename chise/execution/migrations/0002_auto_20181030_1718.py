# Generated by Django 2.1.2 on 2018-10-30 17:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
        ('execution', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='execution',
            name='module',
        ),
        migrations.AddField(
            model_name='execution',
            name='modules',
            field=models.ManyToManyField(to='core.Module', verbose_name='Modules'),
        ),
    ]
