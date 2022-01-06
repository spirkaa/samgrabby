from django.contrib import admin

from . import models


class DownLinkInline(admin.TabularInline):
    model = models.DownLink
    extra = 5


class SoftAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["name", "version", "url_key"]}),
        ("Date information", {"fields": ["upd_date"]}),
    ]
    inlines = [DownLinkInline]
    list_display = ("name", "version", "upd_date")
    list_filter = ["upd_date"]
    search_fields = ["name"]


admin.site.register(models.Soft, SoftAdmin)
