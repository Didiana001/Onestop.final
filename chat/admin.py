from django.contrib import admin
from .models import Letter

@admin.register(Letter)
class LetterAdmin(admin.ModelAdmin):
    list_display = ('title', 'letter_type', 'file')
    search_fields = ('title', 'letter_type')
