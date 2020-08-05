from django.contrib import admin
from order.models import Order, OrderItem

# Register your models here.


class OrderAdmin(admin.ModelAdmin):
	list_display = ('user', 'registered_dttm')


class OrderItemAdmin(admin.ModelAdmin):
	list_display = ('product', 'order')


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)