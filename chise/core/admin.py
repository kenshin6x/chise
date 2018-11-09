# -*- coding: utf-8 -*-

from chise import settings
from django.contrib.auth.models import Permission
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin
from django.forms import TextInput, Textarea
from django.db import models
from django.utils.safestring import mark_safe
from django.urls import reverse, resolve
from django.http import JsonResponse
from django.core import serializers
from django.conf.urls import url
from django.urls import reverse, resolve
from chise.core.models import *

@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    pass

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_variables',)
    filter_horizontal = ('variables',)
    search_fields = ('name',
                    'variables__name',
                    'variables__value',
                    'variables__description',)

    def get_variables(self, object):
        return mark_safe('</br>'.join([str(o) for o in object.variables.all()]))

    get_variables.short_description = _('Variables')


@admin.register(Variable)
class VariableAdmin(admin.ModelAdmin):
    list_display = ('name', 
                'value', 
                'request_method', 
                'description',)
    list_display_links = ('name', 
                    'value', 
                    'request_method',)
    search_fields = ('description',
                    'name',
                    'value',
                    'request_method',)
    list_filter = ('request_method',)


@admin.register(Script)
class ScriptAdmin(admin.ModelAdmin):
    list_display = ('group', 
                    'name',
                    'url_sufix',
                    'get_variables')
    list_display_links = ('group',
                        'name',
                        'url_sufix')
    search_fields = ('group__name',
                    'name',
                    'url_sufix',
                    'variables__name'
                    'variables__value',
                    'description',)
    list_filter = ('group__name',)
    filter_horizontal = ('variables',)

    def get_variables(self, object):
        return mark_safe('</br>'.join([str(o) for o in object.variables.all()]))

    get_variables.short_description = _('Variables')

    class Media:
        js = (
            settings.STATIC_URL  + 'codemirror/lib/codemirror.js',
            settings.STATIC_URL  + 'codemirror/mode/python/python.js',
            settings.STATIC_URL  + 'codemirror/addon/hint/show-hint.js',
            settings.STATIC_URL  + 'js/codemirror-init.js',
        )
        css = {'all': (
                settings.STATIC_URL  + 'codemirror/lib/codemirror.css',
                settings.STATIC_URL  + 'codemirror/theme/monokai.css',
            )
        }


class ScriptsInline(admin.StackedInline):
    model = Module.scripts.through
    extra = 0
    min_num = 1

    def get_formset(self, request, object=None, **kwargs):
        self.parent_object = object
        return super().get_formset(request, object, **kwargs)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if self.parent_object is not None:
            qs = Script.objects.filter(group=self.parent_object.group)
            kwargs['queryset'] = qs

        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('group',
                    'name',
                    'get_scripts',
                    'get_variables',
                    'description',)
    list_display_links = ('group',
                        'name',)
    search_fields = ('group__name',
                    'name',
                    'scripts__name',
                    'scripts__url_sufix',
                    'variables__name',
                    'variables__value',
                    'description',)
    list_filter = ('group',)
    filter_horizontal = ('variables', )
    fieldsets = (
            ('', {'fields' : ('name',
                            'group',
                            'description',
                            'variables',)}),
    )

    def get_variables(self, object):
        return mark_safe('</br>'.join([str(o) for o in object.variables.all()]))

    def get_scripts(self, object):
        return mark_safe('</br>'.join([o.name for o in object.scripts.all()]))

    get_variables.short_description = _('Variables')
    get_scripts.short_description = _('Scripts')

    def get_readonly_fields(self, request, obj=None):
        fields = []
        
        if obj is not None:
            fields.append('group')
            self.inlines = (ScriptsInline, )
        else:
            self.inlines = ()
            
        return fields

    class Media:
        js = (
            settings.STATIC_URL  + 'js/core/module-form-events.js',
        )
        css = {'all': (
            )
        }


@admin.register(Site)
class SiteAdmin(admin.ModelAdmin):
    list_display = ('group',
                    'name',
                    'url_base',
                    'get_variables',)
    list_display_links = ('group',
                        'name',
                        'url_base',)
    filter_horizontal = ('variables',)
    search_fields = ('group__name',
                    'name',
                    'url_base',
                    'variables__name',
                    'variables__value',
                    'variables__description',)
    list_filter = ('group__name',)


    def get_variables(self, object):
        return mark_safe('</br>'.join([str(o) for o in object.variables.all()]))

    get_variables.short_description = _('Variables')

