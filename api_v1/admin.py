from django.contrib import admin
from .models import Developer, Game, Order


@admin.register(Developer)
class DeveloperAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'country', 'established_year')
    search_fields = ('name', 'country')


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'genre', 'price', 'developer', 'is_available')
    list_filter = ('genre', 'is_available', 'developer')
    search_fields = ('title',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer_email', 'game', 'status', 'order_date')
    list_filter = ('status', 'order_date')