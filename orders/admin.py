from django.contrib import admin

from orders.models import Order


class OrderAdmin(admin.ModelAdmin):
    list_display = ['customer', 'robot_serial', 'robot_version']


admin.site.register(Order, OrderAdmin)