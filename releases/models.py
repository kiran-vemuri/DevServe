from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
import os

# Create your models here.


@python_2_unicode_compatible
class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, blank=False, unique=True)
    create_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Component(models.Model):
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=200,blank=False, unique=True)
    create_date = models.DateTimeField(auto_now_add=True)
    component_owner = models.CharField(max_length=200, default="No Owner Specified")

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Binary(models.Model):
    id = models.AutoField(primary_key=True)
    component = models.ForeignKey(Component, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=300, blank=False)
    path = models.FilePathField(max_length=1000)
    url = models.CharField(max_length=1000, default="#")
    notes = models.CharField(max_length=2000, blank=False, default="*No Notes Provided*")
    status = models.CharField(max_length=20, blank=False, default="new")
    change_notes = models.CharField(max_length=2000, blank=False, default="*No Notes Provided*")
    bug_url = models.URLField(max_length=1000, blank=True)
    upload_date = models.DateTimeField(auto_now_add=True)
    status_change_date = models.DateTimeField(auto_now=True)
    md5sum = models.CharField(max_length=40, default="Not Available")

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class EventLog(models.Model):
    id = models.AutoField(primary_key=True)
    binary = models.ForeignKey(Binary, on_delete=models.CASCADE, null=True)
    event_date = models.DateTimeField(auto_now_add=True)
    event_log = models.TextField(default="No event log")

    def __str__(self):
        return self.event_log
