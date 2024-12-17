from django.contrib import admin
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    # Список полей, отображаемых в списке задач
    list_display = ('title', 'project', 'assigned_to', 'status', 'deadline', 'created_at')

    # Фильтры для быстрого поиска и фильтрации
    list_filter = ('status', 'project', 'assigned_to', 'deadline')

    # Поиск по полям
    search_fields = ('title', 'description', 'assigned_to__username', 'project__title')

    # Поля, отображаемые на странице редактирования задачи
    fieldsets = (
        (None, {
            'fields': ('project', 'title', 'description', 'assigned_to', 'status', 'deadline')
        }),
        ('Дополнительная информация', {
            'fields': ('solution', 'code_branch'),
            'classes': ('collapse',)  # Сворачиваемый блок
        }),
    )

    # Поля, доступные только для чтения
    readonly_fields = ('created_at',)

    # Сортировка по умолчанию
    ordering = ('-created_at',)

    # Настройка отображения даты и времени
    date_hierarchy = 'created_at'

    # Настройка формы редактирования
    save_on_top = True  # Кнопки сохранения вверху страницы
    save_as = True  # Возможность сохранить как новую задачу