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
        "updated_at",
    )
    list_filter = ("category", "audience", "related_priority", "published")
    search_fields = ("title", "summary", "body")
    prepopulated_fields = {"slug": ("title",)}
