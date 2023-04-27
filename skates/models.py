from django.db import models


class Skate(models.Model):
    name = models.CharField(max_length=120, default='skate', verbose_name='Название')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    price = models.FloatField(default=10, verbose_name='Цена')
    article_number = models.IntegerField(verbose_name='Артикул')
    color = models.CharField(max_length=30, verbose_name='Цвет')
    date_create = models.DateField(auto_now_add=True, verbose_name='Дата создания')
    date_update = models.DateTimeField(auto_now=True, null=True, verbose_name='Дата изменения')
    photo = models.ImageField(upload_to='image/%Y/%m/%d', null=True, verbose_name='Фото')
    exist = models.BooleanField(default=True, verbose_name='Доступно')

    def __str__(self):
        """Переопределение названия объекта"""
        return self.name  # В админке возвращается название

    class Meta:
        """Класс для названия модели Skate в админке"""
        verbose_name = 'Скейт'  # Название в единственном числе
        verbose_name_plural = 'Скейтборды'  # Название во множественном числе
        ordering = ['-name']  # Сортировка полей по убыванию (-)
