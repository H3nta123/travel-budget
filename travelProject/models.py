from django.db import models
from django.utils import timezone


class Trip(models.Model):
    """Модель путешествия (например, 'Тайланд 2024')"""
    name = models.CharField("Название поездки", max_length=100)
    start_date = models.DateField("Дата начала", default=timezone.now)
    end_date = models.DateField("Дата конца", blank=True, null=True)
    budget = models.DecimalField("Общий бюджет", max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Путешествие"
        verbose_name_plural = "Путешествия"


class Expense(models.Model):
    """Модель конкретной траты"""
    CATEGORY_CHOICES = [
        ('food', 'Еда'),
        ('transport', 'Транспорт'),
        ('stay', 'Жилье'),
        ('entertainment', 'Развлечения'),
        ('shopping', 'Шоппинг'),
        ('other', 'Прочее'),
    ]

    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='expenses', verbose_name="Поездка")
    title = models.CharField("Название траты", max_length=100)
    amount = models.DecimalField("Сумма", max_digits=10, decimal_places=2)
    category = models.CharField("Категория", max_length=20, choices=CATEGORY_CHOICES, default='other')
    date = models.DateField("Дата", default=timezone.now)

    def __str__(self):
        return f"{self.title} ({self.amount})"

    class Meta:
        verbose_name = "Расход"
        verbose_name_plural = "Расходы"