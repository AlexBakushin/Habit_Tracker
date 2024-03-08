from django.contrib import admin
from .models import Habit


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    """
    Регистрация модели Habit в админке
    """
    list_display = ('action', 'time', 'is_pleasant_habit', 'is_published')
    list_filter = ('action',)
    search_fields = ('action',)
