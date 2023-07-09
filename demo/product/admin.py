from __future__ import annotations

from django.contrib import admin

from .models import Brand, Product, ProductImage


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
    ]
    search_fields = [
        "id",
        "name",
    ]
    list_display_links = [
        "id",
    ]


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    autocomplete_fields = [
        "product",
    ]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
        "price",
    ]
    search_fields = [
        "id",
        "name",
    ]
    list_display_links = [
        "id",
    ]
    autocomplete_fields = [
        "brand",
    ]
    inlines = [
        ProductImageInline,
    ]
