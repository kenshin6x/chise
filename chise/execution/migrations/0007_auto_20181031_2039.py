# Generated by Django 2.1.2 on 2018-10-31 20:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('execution', '0006_execution_variables'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='execution',
            name='date_execution_began',
        ),
        migrations.AddField(
            model_name='execution',
            name='date_execution_started',
            field=models.DateTimeField(null=True, verbose_name='Date Execution Started'),
        ),
        migrations.AlterField(
            model_name='checkpoint',
            name='reference',
            field=models.IntegerField(choices=[(1, 'START'), (2, 'END'), (3, 'RUNTIME')], null=True, verbose_name='Reference'),
        ),
    ]
