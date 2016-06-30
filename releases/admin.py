from django.contrib import admin

from .models import Product, Component, Binary

# Register your models here.

admin.site.register(Product)
admin.site.register(Component)
admin.site.register(Binary)
