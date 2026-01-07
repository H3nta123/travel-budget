from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Trip(models.Model):
    """Модель путешествия (например, 'Тайланд 2024')"""
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='trips', 
        verbose_name="Владелец",
        null=True,
        blank=True
    )
    name = models.CharField("Название поездки", max_length=100)
    start_date = models.DateField("Дата начала", default=timezone.now)
    end_date = models.DateField("Дата конца", blank=True, null=True)
    budget = models.DecimalField("Общий бюджет", max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Путешествие"
        verbose_name_plural = "Путешествия"



class Currency(models.Model):
    """Модель валюты"""
    code = models.CharField("Код валюты", max_length=3, unique=True, help_text="ISO код, например USD")
    name = models.CharField("Название", max_length=50)
    rate_to_rub = models.DecimalField("Курс к рублю", max_digits=10, decimal_places=4, default=1.0)
    
    def __str__(self):
        return self.code

    class Meta:
        verbose_name = "Валюта"
        verbose_name_plural = "Валюты"


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
    amount = models.DecimalField("Сумма в валюте", max_digits=10, decimal_places=2)
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT, verbose_name="Валюта", null=True, blank=True)
    category = models.CharField("Категория", max_length=20, choices=CATEGORY_CHOICES, default='other')
    date = models.DateField("Дата", default=timezone.now)

    def __str__(self):
        return f"{self.title} ({self.amount} {self.currency.code if self.currency else 'RUB'})"
    
    @property
    def amount_in_rub(self):
        if self.currency:
            return self.amount * self.currency.rate_to_rub
        return self.amount

    class Meta:
        verbose_name = "Расход"
        verbose_name_plural = "Расходы"