import json
from django.shortcuts import render, get_object_or_404
from django.db.models import Sum
from .models import Trip


def index(request):
    """Главная страница: список всех путешествий"""
    trips = Trip.objects.all().order_by('-start_date')
    return render(request, 'travelProject/index.html', {'trips': trips})


def trip_detail(request, trip_id):
    """Страница конкретного путешествия с расходами и графиками"""
    trip = get_object_or_404(Trip, pk=trip_id)
    expenses = trip.expenses.all().order_by('-date')

    # Calculate totals
    total_spent = sum(exp.amount for exp in expenses)
    remaining_budget = trip.budget - total_spent

    # Prepare data for category pie chart
    category_data = trip.expenses.values('category').annotate(
        total=Sum('amount')
    ).order_by('-total')

    categories = []
    amounts = []
    category_names = dict(trip.expenses.model.CATEGORY_CHOICES)

    for item in category_data:
        categories.append(category_names.get(item['category'], item['category']))
        amounts.append(float(item['total']))

    # Prepare data for timeline bar chart
    daily_data = trip.expenses.values('date').annotate(
        total=Sum('amount')
    ).order_by('date')

    dates = []
    daily_amounts = []

    for item in daily_data:
        dates.append(item['date'].strftime('%d.%m'))
        daily_amounts.append(float(item['total']))

    context = {
        'trip': trip,
        'expenses': expenses,
        'total_spent': total_spent,
        'remaining_budget': remaining_budget,
        # JSON data for charts
        'categories_json': json.dumps(categories, ensure_ascii=False),
        'amounts_json': json.dumps(amounts),
        'dates_json': json.dumps(dates),
        'daily_amounts_json': json.dumps(daily_amounts),
    }
    return render(request, 'travelProject/trip_detail.html', context)