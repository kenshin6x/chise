# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from chise.execution import constants
from chise.core import models as core_models

class Keyword(models.Model):
    name = models.CharField(_('Name'),
                        unique=True,
                        max_length=255,
                        null=False,
                        blank=False)

    class Meta:
        verbose_name = _('Keyword')
        verbose_name_plural = _('Keywords')
        ordering = ['name']


    def __str__(self):
        return u'%s' % self.name


class Checkpoint(models.Model):
    name = models.CharField(_('Name'),
                        max_length=255,
                        null=False,
                        blank=False)
    status = models.IntegerField(_('Status'),
                                choices=constants.STATUS_CHOICES,
                                null=True,
                                blank=False)
    object = models.IntegerField(_('Object'),
                                choices=constants.OBJECT_CHOICES,
                                null=True,
                                blank=False)
    reference = models.IntegerField(_('Reference'),
                                choices=constants.REFERENCE_CHOICES,
                                null=True,
                                blank=False)
    description = models.TextField(_('Description'),
                                null=True,
                                blank=True)
    date_checkpoint = models.DateTimeField(_('Date Checkpoint'),
                                        auto_now_add=True,
                                        null=False,
                                        blank=False)

    class Meta:
        verbose_name = _('Checkpoint')
        verbose_name_plural = _('Checkpoints')
        ordering = ['pk']


    def __str__(self):
        return u'%s [%s]' % (self.name, self.date_checkpoint)


class Execution(models.Model):
    site = models.ForeignKey(core_models.Site,
                            on_delete=models.PROTECT,
                            verbose_name=_('Site'),
                            blank=False,
                            null=True)
    modules = models.ManyToManyField(core_models.Module,
                                verbose_name=_('Modules'))
    description = models.TextField(_('Description'),
                                null=True,
                                blank=True)
    keywords = models.ManyToManyField('keyword',
                                    verbose_name=_('Keywords'),
                                    blank=True)
    checkpoints = models.ManyToManyField('checkpoint',
                                    verbose_name=_('Checkpoints'),
                                    blank=True)
    variables = models.ManyToManyField(core_models.Variable,
                                    verbose_name=_('Variables'),
                                    blank=True)
    user_created = models.ForeignKey(User,
                                    on_delete=models.PROTECT,
                                    verbose_name=_('User Created'),
                                    null=False,
                                    blank=False)
    date_created = models.DateTimeField(_('Date Created'),
                                        auto_now_add=True,
                                        null=False,
                                        blank=False)
    date_started = models.DateTimeField(_('Date Started'),
                                                auto_now_add=False,
                                                null=True,
                                                blank=False)
    date_finished = models.DateTimeField(_('Date Finished'),
                                                    auto_now_add=False,
                                                    null=True,
                                                    blank=False)

    class Meta:
        verbose_name = _('Execution')
        verbose_name_plural = _('Execution')
        ordering = ['-pk']
        permissions = (
                ('can_execute', _('Can execute execution')),
                ('can_reexecute', _('Can re-execute execution')),
        )

    def __str__(self):
        if self.description is not None:
            return u'%s' % self.description
        else:
            return u'%s' % self.site

    def is_started(self):
        if self.date_started is not None:
            return True
        else:
            return False

    def is_running(self):
        if self.date_started is not None \
            and self.date_finished is None:
            return True
        else:
            return False

    def is_finished(self):
        if self.date_finished is not None:
            return True
        else:
            return False

    def status(self):
        if self.is_finished():
            return _('Finished')
        elif self.is_running():
            return _('Running')
        else:
            return _('Waiting')






