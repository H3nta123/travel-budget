from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'travelProject'

urlpatterns = [
    # Главная
    path('', views.index, name='index'),
    
    # Авторизация
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    # Путешествия (CRUD)
    path('trip/new/', views.trip_create, name='trip_create'),
    path('trip/<int:trip_id>/', views.trip_detail, name='trip_detail'),
    path('trip/<int:trip_id>/edit/', views.trip_edit, name='trip_edit'),
    path('trip/<int:trip_id>/delete/', views.trip_delete, name='trip_delete'),
    
    # Расходы
    path('trip/<int:trip_id>/expense/add/', views.expense_add, name='expense_add'),
    path('trip/<int:trip_id>/expense/<int:expense_id>/delete/', views.expense_delete, name='expense_delete'),
]