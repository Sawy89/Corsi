from django.contrib import admin
from django.utils.html import mark_safe

from .models import *

# Register your models here.
admin.site.register(DishCategory)
admin.site.register(Dish)
admin.site.register(DishPrice)
admin.site.register(Topping)
admin.site.register(Addition)

# https://developer.mozilla.org/it/docs/Learn/Server-side/Django/Admin_site
class OrdersAdmin(admin.ModelAdmin):
    list_display = ('user','insertdate','completed','countDish','total_price')
    list_filter = ('user','completed')
    readonly_fields = ['user','insertdate','countDish','list_dishes']

    fieldsets = (
        (None, {
            'fields': ('user','insertdate','countDish')
        }),
        ('Dishes', {
            'fields': ('list_dishes',)
        }),
        ('Status', {
            'fields': ('completed','insertdate_completed')
        }),
    )

    def list_dishes(self, obj):
        '''
        Prepare the list in HTML
        https://stackoverflow.com/questions/43132069/django-admin-list-display-product-list
        '''
        str_list = obj.getDishes()
        # each obj will be an Order obj/instance/row
        to_return = '<ul>'
        # I'm assuming that there is a name field under the event.Product model. If not change accordingly.
        for item in str_list:
            to_return += ''.join('<li>'+item+'</li>')
        to_return += '</ul>'
        return mark_safe(to_return)


admin.site.register(Orders, OrdersAdmin)