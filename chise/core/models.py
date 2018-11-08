# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _
from chise.core import constants

class Variable(models.Model):
    name = models.CharField(_('Name'),
                        max_length=255,
                        null=False,
                        blank=False)
    value = models.CharField(_('Value'),
                        max_length=255,
                        null=False,
                        blank=False)
    request_method = models.IntegerField(_('Method'),
                                        choices=constants.REQUEST_CHOICES,
                                        default=constants.REQUEST_GET,
                                        null=False,
                                        blank=False)
    description = models.TextField(_(u'Description'),
                                null=True,
                                blank=True)

    class Meta:
        unique_together = (('name', 'value', 'request_method'), )
        verbose_name = _('Variable')
        verbose_name_plural = _('Variables')
        ordering = ['description', 'name', 'value']


    def __str__(self):
        text = u'(%s) %s = %s' % (self.get_request_method_display(),
                                self.name,
                                self.value)
        if self.description:
            text =  '%s (%s)' % (text, self.description)
            
        return text


class Group(models.Model):
    name = models.CharField(_('Name'),
                        unique=True,
                        max_length=255,
                        null=False,
                        blank=False)
    variables = models.ManyToManyField('Variable',
                                    verbose_name=_('Variables'),
                                    blank=True)

    class Meta:
        verbose_name = _('Group')
        verbose_name_plural = _('Groups')
        ordering = ['name']

    def __str__(self):
        return u'%s' % self.name


class Script(models.Model):
    group = models.ForeignKey('Group',
                            on_delete=models.PROTECT,
                            verbose_name=_('Group'),
                            null=False,
                            blank=False)
    name = models.CharField(_('Name'),
                            max_length=255,
                            null=False,
                            blank=False)
    url_sufix = models.CharField(_('URL Sufix'),
                                max_length=1000,
                                null=True,
                                blank=True)
    variables = models.ManyToManyField('Variable',
                                    verbose_name=_('Variables'),
                                    blank=True)
    code = models.TextField(_('Code'),
                            null=True,
                            blank=True)

    class Meta:
        verbose_name = _('Script')
        verbose_name_plural = _('Scripts')
        ordering = ['group', 'name']

    def __str__(self):
        return u'%s - %s' % (self.group, self.name)


class Module(models.Model):
    group = models.ForeignKey('Group',
                            on_delete=models.PROTECT,
                            verbose_name=_('Group'),
                            null=False,
                            blank=False)
    name = models.CharField(_('Name'),
                        max_length=255,
                        null=False,
                        blank=False)
    description = models.TextField(_('Description'),
                                null=True,
                                blank=True)
    scripts = models.ManyToManyField('Script',
                                    verbose_name=_('Scripts'),
                                    blank=False)
    variables = models.ManyToManyField('Variable',
                                    verbose_name=_('Variables'),
                                    blank=True)

    class Meta:
        unique_together = (('group', 'name'), )
        verbose_name = _('Module')
        verbose_name_plural = _('Module')
        ordering = ['name']

    def __str__(self):
        return u'%s' % self.name


class Site(models.Model):
    group = models.ForeignKey('Group',
                            verbose_name=_('Group'),
                            on_delete=models.PROTECT,
                            null=False,
                            blank=False)
    name = models.CharField(_('Name'),
                        max_length=255,
                        null=False,
                        blank=False)
    url_base = models.URLField(_('URL Base'),
                            null=False,
                            blank=False)
    variables = models.ManyToManyField('Variable',
                                    verbose_name=_('Variables'),
                                    blank=True)

    class Meta:
        unique_together = (('group', 'name'), )
        verbose_name = _('Site')
        verbose_name_plural = _('Sites')
        ordering = ['group', 'name']

    def __str__(self):
        return u'%s - %s' % (self.group, self.name)


