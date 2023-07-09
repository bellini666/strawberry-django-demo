from __future__ import annotations

from django.contrib import admin

from .models import Cart, CartItem, Order, OrderItem


class CartItemInline(admin.TabularInline):
    model = CartItem
    autocomplete_fields = [
        "cart",
        "product",
    ]


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "status",
    ]
    search_fields = [
        "id",
    ]
    list_display_links = [
        "id",
    ]
    inlines = [
        CartItemInline,
    ]


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    autocomplete_fields = [
        "order",
        "product",
    ]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "user",
    ]
    search_fields = [
        "id",
    ]
    list_display_links = [
        "id",
    ]
    autocomplete_fields = [
        "user",
        "cart",
    ]
    inlines = [
        OrderItemInline,
    ]
