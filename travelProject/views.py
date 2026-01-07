import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from .models import Trip, Expense
from .forms import CustomUserCreationForm, TripForm, ExpenseForm


def register(request):
    """Регистрация нового пользователя"""
    if request.user.is_authenticated:
        return redirect('travelProject:index')
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Добро пожаловать, {user.username}! Аккаунт создан.')
            return redirect('travelProject:index')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'registration/register.html', {'form': form})


def index(request):
    """Главная страница: список путешествий пользователя"""
    if request.user.is_authenticated:
        trips = Trip.objects.filter(user=request.user).order_by('-start_date')
    else:
        trips = Trip.objects.none()
    return render(request, 'travelProject/index.html', {'trips': trips})


@login_required
def trip_detail(request, trip_id):
    """Страница конкретного путешествия с расходами и графиками"""
    trip = get_object_or_404(Trip, pk=trip_id, user=request.user)
    expenses = trip.expenses.all().select_related('currency').order_by('-date')

    total_spent = sum(exp.amount_in_rub for exp in expenses)
    remaining_budget = trip.budget - total_spent

    category_totals = {}
    category_names = dict(Expense.CATEGORY_CHOICES)
    
    for exp in expenses:
        cat_name = category_names.get(exp.category, exp.category)
        if cat_name not in category_totals:
            category_totals[cat_name] = 0
        category_totals[cat_name] += float(exp.amount_in_rub)
    
    sorted_cats = sorted(category_totals.items(), key=lambda x: x[1], reverse=True)
    categories = [k for k, v in sorted_cats]
    amounts = [v for k, v in sorted_cats]

    daily_totals = {}
    for exp in expenses:
        date_str = exp.date.strftime('%d.%m')
        if date_str not in daily_totals:
            daily_totals[date_str] = 0
        daily_totals[date_str] += float(exp.amount_in_rub)
        
    dates = sorted(daily_totals.keys())
    daily_amounts = [daily_totals[d] for d in dates]

    context = {
        'trip': trip,
        'expenses': expenses,
        'total_spent': total_spent,
        'remaining_budget': remaining_budget,
        'categories_json': json.dumps(categories, ensure_ascii=False),
        'amounts_json': json.dumps(amounts),
        'dates_json': json.dumps(dates),
        'daily_amounts_json': json.dumps(daily_amounts),
        'daily_amounts_json': json.dumps(daily_amounts),
        'chart_image': get_plot(category_totals)
    }
    return render(request, 'travelProject/trip_detail.html', context)

def get_plot(data):
    """Генерация графика Matplotlib в base64"""
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import io
    import base64

    if not data:
        return None

    plt.figure(figsize=(6, 4))
    plt.pie(data.values(), labels=data.keys(), autopct='%1.1f%%', startangle=140)
    plt.title('Расходы по категориям (Matplotlib)')
    plt.axis('equal') 

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    plt.close()

    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')
    return graphic


@login_required
def trip_create(request):
    """Создание нового путешествия"""
    if request.method == 'POST':
        form = TripForm(request.POST)
        if form.is_valid():
            trip = form.save(commit=False)
            trip.user = request.user
            trip.save()
            messages.success(request, f'Путешествие "{trip.name}" создано!')
            return redirect('travelProject:trip_detail', trip_id=trip.id)
    else:
        form = TripForm()
    
    return render(request, 'travelProject/trip_form.html', {
        'form': form,
        'title': 'Новое путешествие'
    })


@login_required
def trip_edit(request, trip_id):
    """Редактирование путешествия"""
    trip = get_object_or_404(Trip, pk=trip_id, user=request.user)
    
    if request.method == 'POST':
        form = TripForm(request.POST, instance=trip)
        if form.is_valid():
            form.save()
            messages.success(request, 'Путешествие обновлено!')
            return redirect('travelProject:trip_detail', trip_id=trip.id)
    else:
        form = TripForm(instance=trip)
    
    return render(request, 'travelProject/trip_form.html', {
        'form': form,
        'title': f'Редактировать: {trip.name}',
        'trip': trip
    })


@login_required
def trip_delete(request, trip_id):
    """Удаление путешествия"""
    trip = get_object_or_404(Trip, pk=trip_id, user=request.user)
    
    if request.method == 'POST':
        name = trip.name
        trip.delete()
        messages.success(request, f'Путешествие "{name}" удалено.')
        return redirect('travelProject:index')
    
    return render(request, 'travelProject/trip_confirm_delete.html', {'trip': trip})


@login_required
def expense_add(request, trip_id):
    """Добавление расхода к путешествию"""
    trip = get_object_or_404(Trip, pk=trip_id, user=request.user)
    
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.trip = trip
            expense.save()
            messages.success(request, f'Расход "{expense.title}" добавлен!')
            return redirect('travelProject:trip_detail', trip_id=trip.id)
    else:
        form = ExpenseForm()
    
    return render(request, 'travelProject/expense_form.html', {
        'form': form,
        'trip': trip,
        'title': 'Добавить расход'
    })


@login_required
def expense_delete(request, trip_id, expense_id):
    """Удаление расхода"""
    trip = get_object_or_404(Trip, pk=trip_id, user=request.user)
    expense = get_object_or_404(Expense, pk=expense_id, trip=trip)
    
    if request.method == 'POST':
        expense.delete()
        messages.success(request, 'Расход удалён.')
        return redirect('travelProject:trip_detail', trip_id=trip.id)
    
    return render(request, 'travelProject/expense_confirm_delete.html', {
        'expense': expense,
        'trip': trip
    })