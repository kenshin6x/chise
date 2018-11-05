# Generated by Django 2.1.2 on 2018-10-30 14:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='Name')),
            ],
        ),
        migrations.CreateModel(
            name='Module',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('url_sufix', models.CharField(blank=True, max_length=1000, null=True, verbose_name='URL Sufix')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.Group', verbose_name='Group')),
            ],
        ),
        migrations.CreateModel(
            name='Site',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('url_base', models.URLField(verbose_name='URL Base')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.Group', verbose_name='Group')),
            ],
        ),
        migrations.CreateModel(
            name='Variable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('value', models.CharField(max_length=255, verbose_name='Value')),
                ('request_method', models.IntegerField(choices=[(1, 'GET'), (2, 'POST')], default=1, verbose_name='Method')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
            ],
        ),
        migrations.AddField(
            model_name='site',
            name='variables',
            field=models.ManyToManyField(blank=True, to='core.Variable', verbose_name='Variables'),
        ),
        migrations.AddField(
            model_name='module',
            name='variables',
            field=models.ManyToManyField(blank=True, to='core.Variable', verbose_name='Variables'),
        ),
        migrations.AddField(
            model_name='group',
            name='variables',
            field=models.ManyToManyField(blank=True, to='core.Variable', verbose_name='Variables'),
        ),
    ]
