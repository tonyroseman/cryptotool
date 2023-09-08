# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.apps import AppConfig
from django.core.signals import request_started
from django.dispatch import receiver

import time
import sys

class AdminGradientConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'home'
   

    