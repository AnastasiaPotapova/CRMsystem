from django.db import models

## Эта модель была создана для примера и тестов
## В реальном проекте она может быть не нужна
## Пока удалять её не буду так как уже поздно и мне лень
## Если что потом удалю


class User(models.Model):
    id = models.CharField(max_length=200, primary_key=True, unique=True)              
    role = models.CharField(max_length=50)               
    card_id = models.CharField(max_length=100, unique=True)  
    td_username = models.CharField(max_length=150, unique=True) 
    fullname = models.CharField(max_length=255, blank=True)  # добавлено поле fullname
    excursions = models.TextField(blank=True)           

    @property
    def visit_count(self):
        """Количество посещений пользователя (число связанных Visit)."""
        return self.visits.count()

class Visit(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='visits')
    # excursion = models.CharField(max_length=200, blank=True)
    visited_at = models.DateTimeField()

    class Meta:
        db_table = 'hello_visit'
        indexes = [
            models.Index(fields=['visited_at']),
            models.Index(fields=['user', 'visited_at']),
        ]