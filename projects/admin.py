from django.contrib import admin
from .models import Application, Evaluation, Project, TeacherApplication

@admin.register(TeacherApplication)
class TeacherApplicationAdmin(admin.ModelAdmin):
    # Поля, которые будут отображаться в списке заявок
    list_display = ('title', 'created_by', 'created_at', 'description_short', 'requirements_short')
    
    # Поля, по которым можно фильтровать заявки
    list_filter = ('created_by', 'created_at')
    
    # Поля, по которым можно выполнять поиск
    search_fields = ('title', 'description', 'requirements', 'created_by__username')
    
    # Поля, которые будут отображаться в форме редактирования
    fields = ('title', 'description', 'requirements', 'created_by')
    
    # Метод для отображения краткого описания
    def description_short(self, obj):
        return obj.description[:50] + '...' if len(obj.description) > 50 else obj.description
    description_short.short_description = 'Описание'
    
    # Метод для отображения краткого текста требований
    def requirements_short(self, obj):
        return obj.requirements[:50] + '...' if len(obj.requirements) > 50 else obj.requirements
    requirements_short.short_description = 'Требования'

# Регистрация модели Application
@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('project_title', 'applicant', 'leader', 'supervisor', 'applied_at', 'status')
    list_filter = ('status', 'applied_at', 'supervisor')
    search_fields = ('project_title', 'applicant__username', 'leader__username', 'supervisor__username')
    readonly_fields = ('applied_at',)

    fieldsets = (
        (None, {
            'fields': ('applicant', 'project_title', 'project_description')
        }),
        ('Команда', {
            'fields': ('leader', 'team_members')
        }),
        ('Руководитель', {
            'fields': ('supervisor',)
        }),
        ('Статус', {
            'fields': ('status',)
        }),
    )
# Встроенный класс для модели Evaluation
class EvaluationInline(admin.TabularInline):  # Или admin.StackedInline, если нужен другой стиль
    model = Evaluation
    extra = 1  # Количество пустых форм для добавления новых оценок
    readonly_fields = ('created_at',)  # Поля, которые нельзя редактировать
    
# Регистрация модели Project
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_by', 'leader', 'created_at')
    list_filter = ('created_at', 'created_by', 'leader')
    search_fields = ('title', 'created_by__username', 'leader__username')
    readonly_fields = ('created_at',)

    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'created_by')
        }),
        ('Команда', {
            'fields': ('leader', 'members')
        }),
    )
    # Добавляем встроенный класс
    inlines = [EvaluationInline]