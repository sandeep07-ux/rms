from unicodedata import category
from django.contrib import admin
from .models import Category, Customer, Cart, MenuItem, OrderPlaced

import json
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Count, F, Value


@admin.register(Customer)
class CusotmerAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'name',
                    'address', 'city', 'zipcode', 'province']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'price',
                    'description', 'category', 'slug', 'image']
    prepopulated_fields = {'slug': ('name',)}

    # def changelist_view(self, request, extra_context=None):
    #     # Aggregate new subscribers per day
    #     chart_data = (
    #         MenuItem.objects.annotate(cat=F("category"))
    #         .values("cat")
    #         .annotate(y=Count("id"))
    #         .order_by("-cat")
    #     )

    #     # Serialize and attach the chart data to the template context
    #     as_json = json.dumps(list(chart_data), cls=DjangoJSONEncoder)
    #     extra_context = extra_context or {"chart_data": as_json}

    #     # Call the superclass changelist_view to render the page
    #     return super().changelist_view(request, extra_context=extra_context)


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'item', 'quantity']


@admin.register(OrderPlaced)
class OrderPlacedAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'customer',
                    'item', 'quantity', 'ordered_date', 'status']


admin.site.site_header = "Food Mania"
admin.site.site_title = "Food Mania"
admin.site.index_title = "Food Mania"
