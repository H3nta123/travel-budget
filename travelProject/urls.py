from django.urls import path
from . import views

app_name = 'travelProject'


urlpatterns = [
    path('', views.index, name='index'),
    path('trip/<int:trip_id>/', views.trip_detail, name='trip_detail'),
]