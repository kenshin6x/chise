# -*- coding: utf-8 -*-

from chise import settings
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin
from django.core.management import call_command
from django.utils.safestring import mark_safe
from django.conf.urls import url
from django.urls import reverse, resolve
from django.http import JsonResponse
from django.core import serializers
from django.shortcuts import render
from chise.execution.models import *
from chise.core import models as core_models
from chise.core.tasks import execution_task

@admin.register(Keyword)
class KeywordAdmin(admin.ModelAdmin):
    search_fields = ('name',)


@admin.register(Execution)
class ExecutionAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'site',
                    'get_modules',
                    'get_keywords',
                    'user_created',
                    'date_started',
                    'date_finished',
                    'get_execution_actions',)
    list_display_links = ('id',
                        'site',
                        'get_modules',
                        'get_keywords',)
    search_fields = ('site__name',
                    'modules__name',
                    'date_created',
                    'keywords__name',
                    'checkpoints__name',
                    'checkpoints__status')
    list_filter = ('site__group__name',
                'user_created',
                'checkpoints__date_checkpoint',
                'date_started',
                'date_finished',)
    fieldsets = (
            ('', {'fields' : ('site',
                            'modules',
                            'variables',
                            'keywords',
                            'description')}),
    )
    autocomplete_fields = ('variables', 
                        'keywords',)

    def get_modules(self, object):
        return mark_safe('</br>'.join([str(o) for o in object.modules.all()]))

    def get_variables(self, object):
        return mark_safe('</br>'.join([str(o) for o in object.variables.all()]))

    def get_checkpoints(self, object):
        return mark_safe('</br>'.join([str(o) for o in object.checkpoints.all()]))

    def get_keywords(self, object):
        return mark_safe('</br>'.join([str(o) for o in object.keywords.all()]))

    def get_execution_actions(self, object):
        html = ''
        execute_button_name = _('Execute')

        if object.is_running():
            execute_button_name = _('Running')

        if object.is_finished():
            execute_button_name = _('View')

        html += '<a class="button" href="%s">%s</a>' % (reverse('admin:execution-execute', args=[object.pk]), execute_button_name)

        return mark_safe(html)

    get_modules.short_description = _('Modules')
    get_checkpoints.short_description = _('Checkpoints')
    get_keywords.short_description = _('Keywords')
    get_execution_actions.short_description = _('Actions')

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        return form

    def save_model(self, request, obj, form, change):
        obj.user_created = request.user
        super().save_model(request, obj, form, change)

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
                url(r'^(?P<object_pk>.+)/execute/$',
                    self.admin_site.admin_view(self.execute_view),
                    name='execution-execute',),

                url(r'^(?P<object_pk>.+)/checkpoints/$',
                    self.admin_site.admin_view(self.checkpoints_view),
                    name='execution-checkpoints',),
        ]

        return custom_urls + urls

    def execute_view(self, request, object_pk, *args, **kwargs):
        object = Execution.objects.get(pk=object_pk)

        if object.is_started() is False:
            execution_task.delay(object.pk)

        context = {
            **self.admin_site.each_context(request),
            'opts': self.model._meta,
            'app_label': self.model._meta.app_label,
            'title': '%s: #%s' % (_('Execute'), object.pk),
            'entry': object,
            'object_id': object.pk,
        }

        return render(request, 'admin/execution/execute_action.html',
                                context)

    def checkpoints_view(self, request, object_pk, *args, **kwargs):
        object = Execution.objects.get(pk=object_pk)
        checkpoints = []

        for o in Checkpoint.objects.filter(execution=object).order_by('pk'):
            checkpoints.append({
                'id' : o.pk,
                'name' : o.name,
                'status': o.status,
                'status_display': o.get_status_display(),
                'object': o.object,
                'object_display': o.get_object_display(),
                'reference': o.reference,
                'reference_display': o.get_reference_display(),
                'description': o.description,
                'date_checkpoint': o.date_checkpoint,
            })

        response_data = {
            'id': object.pk,
            'date_started': object.date_started,
            'date_finished': object.date_finished,
            'checkpoints' : checkpoints
        }

        return JsonResponse(response_data, safe=False)

    class Media:
        js = (
            settings.STATIC_URL  + 'js/execution/execution-form-events.js',
            settings.STATIC_URL  + 'js/execution/admin-script.js',
        )
