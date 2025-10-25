from django.db import models
from datetime import datetime

class Poll(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    week_start = models.DateField()
    week_end = models.DateField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Опрос за {self.week_start} - {self.week_end} с {self.excursions.count()} экскурсиями"

    class Meta:
        verbose_name = "Опрос"
        verbose_name_plural = "Опросы"

class Excursion(models.Model):
    date = models.DateTimeField()
    n_visitors = models.IntegerField()
    guide = models.CharField(max_length=100, default="not defined", null=True, blank=True)
    phone = models.CharField(max_length=20)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name="excursions", null=True, blank=True)

    def __str__(self):
        return f"Экскурсия {self.date} (гид: {self.guide})"

    class Meta:
        verbose_name = "Экскурсия"
        verbose_name_plural = "Экскурсии"