from django.contrib import admin
from .models import Link,word
from import_export.admin import ImportExportModelAdmin

# Register your models here.

admin.site.register(word)

@admin.register(Link)
class LinkAdmin(ImportExportModelAdmin):
    pass
