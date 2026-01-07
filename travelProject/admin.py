from django.contrib import admin
from .models import Trip, Expense, Currency

@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'rate_to_rub')
    search_fields = ('code', 'name')

@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'budget')
    search_fields = ('name',)

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('title', 'amount', 'currency', 'category', 'trip', 'date')
    list_filter = ('trip', 'category', 'date', 'currency')
    search_fields = ('title',)