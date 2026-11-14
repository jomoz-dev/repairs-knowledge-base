from django.contrib import admin

from .models import Article, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "typical_trades", "sort_order")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "category",
        "audience",
        "related_priority",
        "published",
        "reviewed_on",
        "reviewed_by",
        "updated_at",
    )
    list_filter = ("category", "audience", "related_priority", "published")
    search_fields = ("title", "summary", "body", "reviewed_by")
    prepopulated_fields = {"slug": ("title",)}
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "category",
                    "title",
                    "slug",
                    "audience",
                    "related_priority",
                    "summary",
                    "body",
                )
            },
        ),
        (
            "Document control",
            {
                "fields": ("published", "reviewed_on", "reviewed_by"),
                "description": "Drafts stay unpublished. Last reviewed is what advisors see on the article.",
            },
        ),
    )
