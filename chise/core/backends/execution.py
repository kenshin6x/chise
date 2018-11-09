#!python
# -*- coding: utf-8 -*-

import os
import sys
import pytz
from time import sleep
from chise import settings
from urllib.parse import urljoin
from furl import furl
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from datetime import datetime
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.db.models import Q
from django.core.management.base import BaseCommand, CommandError
from argparse import ArgumentParser
from bs4 import BeautifulSoup
from chise.core import models as core_models
from chise.core.constants import *
from chise.execution import models as execution_models
from chise.execution.constants import *


class ExecutionException(Exception):
    pass

class NoSuchVariableException(Exception):
    pass


class ExecutionBackend:
    profile = None
    driver = None
    action = None
    html = None

    execution = None
    last_module = None
    last_script = None

    last_script_has_error = None

    def __init__(self, execution_id, *args, **kwargs):
        try:
            self.execution = execution_models.Execution.objects.get(pk=execution_id)
            self.clean_database()
            self.start_execution()

            if len(settings.FIREFOX_PROFILE) > 0:
                self.profile = webdriver.FirefoxProfile(settings.FIREFOX_PROFILE)

        except execution_models.Execution.DoesNotExist:
            print (_('Execution object not found with id=%s' % execution_id))
            exit()

    def parse_html(self, page_source):
        return BeautifulSoup(page_source, 'html.parser')

    def get_html_response(url):
        with urllib.request.urlopen(url) as response:
            return response.read()

    def clean_database(self):
        self.execution.checkpoints.all().delete()
        self.execution.date_started = None
        self.execution.date_finished = None
        self.execution.save()

    def start_execution(self):
        self.execution.date_started = timezone.now()
        self.execution.save()

    def end_execution(self):
        self.execution.date_finished = timezone.now()
        self.execution.save()

    def get_variables(self, q = None):
        variables = {
            settings.PROJECT_CODENAME : 1
        }

        # variables from group
        for o in self.execution.site.group.variables.filter(q):
            variables.update({o.name : o.value})

        # variables from site
        for o in self.execution.site.variables.filter(q):
            variables.update({o.name : o.value})

        # variables from module
        if self.last_module is not None:
            for o in self.last_module.variables.filter(q):
                variables.update({o.name : o.value})

        # variables from script
        if self.last_script is not None:
            for o in self.last_script.variables.filter(q):
                variables.update({o.name : o.value})

        # variables from execution
        for o in self.execution.variables.filter(q):
            variables.update({o.name : o.value})

        return variables

    def get_variable(self, name):
        variables = self.get_variables(Q(name=name))

        if variables.get(name):
            return variables.get(name)
        else:
            raise NoSuchVariableException (name)

    def get_url_base(self):
        return self.execution.site.url_base

    def get_url(self):
        url = self.get_url_base()
        if self.last_script is not None:
            url = urljoin(url, self.last_script.url_sufix)

        variables = self.get_variables(Q(request_method=REQUEST_GET))
        url = furl(url).add(variables).url

        return url

    def add_checkpoint(self, name, object, reference, status, description=None):
        checkpoint = execution_models.Checkpoint()
        checkpoint.date_checkpoint = datetime.now()
        checkpoint.name = name.upper()
        checkpoint.reference = reference
        checkpoint.object = object
        checkpoint.status = status
        checkpoint.description = description
        checkpoint.save()

        self.execution.checkpoints.add(checkpoint)

    def find_element_by_xpath(self, xpath):
        element = self.driver.find_element_by_xpath(xpath)
        self.action.move_to_element(element).perform()
        return element

    def find_elements_by_xpath(self, xpath):
        elements = self.driver.find_elements_by_xpath(xpath)
        self.action.move_to_element(element).perform()
        return elements

    def run(self, *args, **kwargs):
        try:
            try:
                for module in self.execution.modules.all():
                    self.last_module = module
                    self.add_checkpoint(self.last_module.name,
                                        OBJECT_MODULE,
                                        REFERENCE_START,
                                        STATUS_SUCCESS)

                    self.driver = webdriver.Firefox(self.profile,
                                                    executable_path=settings.GECKODRIVER_BIN,
                                                    firefox_binary=settings.FIREFOX_BIN)
                    self.action = ActionChains(self.driver)

                    try:
                        for script in core_models.ModuleScript.objects.filter(module=self.last_module):
                            self.last_script = script.script
                            self.last_script_has_error = False
                            self.add_checkpoint(self.last_script.name,
                                                OBJECT_SCRIPT,
                                                REFERENCE_START,
                                                STATUS_SUCCESS)

                            self.driver.get(self.get_url())
                            self.html = self.parse_html(self.driver.page_source)

                            code = ''
                            for util in self.last_script.utils.all():
                                code += util.code + '\n'

                            code += '\n' + self.last_script.code
                            exec(code)

                            self.add_checkpoint(self.last_script.name,
                                                OBJECT_SCRIPT,
                                                REFERENCE_END,
                                                STATUS_SUCCESS)

                    except Exception as e:
                        self.last_script_has_error = True
                        self.add_checkpoint(self.last_script.name,
                                                OBJECT_SCRIPT,
                                                REFERENCE_RUNTIME,
                                                STATUS_FAIL,
                                                '%s : %s' % (e.__class__.__name__, str(e)))

                    self.add_checkpoint(self.last_module.name,
                                        OBJECT_MODULE,
                                        REFERENCE_END,
                                        STATUS_SUCCESS if self.last_script_has_error is False else STATUS_FAIL)
                    self.driver.close()

            except Exception as e:
                self.add_checkpoint(self.last_module.name,
                                        OBJECT_MODULE,
                                        REFERENCE_RUNTIME,
                                        STATUS_FAIL,
                                        '%s : %s' % (e.__class__.__name__, str(e)))

            self.end_execution()

        except Exception as e:
            self.add_checkpoint(_('Exception'),
                                OBJECT_OTHER,
                                REFERENCE_RUNTIME,
                                STATUS_FAIL,
                                '%s : %s' % (e.__class__.__name__, str(e)))
            self.end_execution()
            self.driver.close()
