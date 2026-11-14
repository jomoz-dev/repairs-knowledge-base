from django.apps import AppConfig


class KnowledgeConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "knowledge"
    verbose_name = "Repairs knowledge"

    def ready(self):
        from django.contrib import admin

        admin.site.site_header = "Repairs Knowledge Base"
        admin.site.site_title = "Knowledge Base"
        admin.site.index_title = "Articles and categories"
