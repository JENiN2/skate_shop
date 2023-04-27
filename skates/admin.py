from django.contrib import admin

from.models import Skate


class SkateAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'article_number', 'exist')  # Отображение полей
    list_display_links = ('id', 'name')  # Установка ссылок на атрибуты
    search_fields = ('name', 'price')  # поиск по полям
    list_editable = ('price', 'exist')  # Изменяемое поле
    list_filter = ('exist', 'color')  # Фильтры полей


admin.site.register(Skate, SkateAdmin)  # (Модель, Форма админки модели)
