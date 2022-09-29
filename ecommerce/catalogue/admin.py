from django.contrib import admin
from django import forms
from mptt.admin import MPTTModelAdmin

from .models import (
    Category,
    ProductType,
    ProductSpecific,
    ProductImage,
    Product,
    ProductSpecificValue,
    ProductBrand
)

admin.site.register(Category, MPTTModelAdmin)

class ProductSpecificInline(admin.TabularInline):
    model = ProductSpecific

@admin.register(ProductBrand)
class ProductBrandAdmin(admin.ModelAdmin):
    pass

@admin.register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    inlines = [ProductSpecificInline]

class ProductImageInline(admin.TabularInline):
    model = ProductImage

class ProductSpecificValueInline(admin.TabularInline):
    model = ProductSpecificValue

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline, ProductSpecificValueInline]
    list_display = ('id', 'product_type', 'title', 'category', 'regular_price')
    ordering = ('-created_at',)


