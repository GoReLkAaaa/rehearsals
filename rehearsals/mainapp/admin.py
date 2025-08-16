from django.contrib import admin
from .models import Product, UserProfile, Purchase, CartItem

# Register your models here.


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name_ru', 'name_uz', 'category', 'price')
    list_filter = ('category',)
    search_fields = ('name_ru', 'name_uz')


admin.site.register(UserProfile)
admin.site.register(Purchase)
admin.site.register(CartItem)