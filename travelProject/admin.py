from django.contrib import admin
from .models import Trip, Expense

@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'budget')
    search_fields = ('name',)

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('title', 'amount', 'category', 'trip', 'date')
    list_filter = ('trip', 'category', 'date')
    search_fields = ('title',)