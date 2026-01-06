from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # Подключаем маршруты нашего приложения к главной странице
    path('', include('travelProject.urls')),
]