from django.contrib import admin
from .models import Link
from import_export.admin import ImportExportModelAdmin

# Register your models here.

@admin.register(Link)
class LinkAdmin(ImportExportModelAdmin):
    pass