from django.db import models
from django.urls import reverse


class Category(models.Model):
    """Repair type, aligned with the Housing Repairs Diagnostic Tool."""

    name = models.CharField(max_length=80)
    slug = models.SlugField(unique=True)
    summary = models.TextField()
    typical_trades = models.CharField(max_length=120, blank=True)
    sort_order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "name"]
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("category_detail", kwargs={"slug": self.slug})


class Article(models.Model):
    AUDIENCE_ADVISOR = "advisor"
    AUDIENCE_RESIDENT = "resident"
    AUDIENCE_CHOICES = [
        (AUDIENCE_ADVISOR, "Advisor procedure"),
        (AUDIENCE_RESIDENT, "Resident guidance"),
    ]

    PRIORITY_EMERGENCY = "emergency"
    PRIORITY_URGENT = "urgent"
    PRIORITY_ROUTINE = "routine"
    PRIORITY_MIXED = "mixed"
    PRIORITY_CHOICES = [
        (PRIORITY_EMERGENCY, "Emergency"),
        (PRIORITY_URGENT, "Urgent"),
        (PRIORITY_ROUTINE, "Routine"),
        (PRIORITY_MIXED, "Depends on answers"),
    ]

    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="articles"
    )
    title = models.CharField(max_length=160)
    slug = models.SlugField(unique=True)
    audience = models.CharField(
        max_length=20, choices=AUDIENCE_CHOICES, default=AUDIENCE_ADVISOR
    )
    related_priority = models.CharField(
        max_length=20, choices=PRIORITY_CHOICES, default=PRIORITY_MIXED
    )
    summary = models.TextField()
    body = models.TextField(
        help_text="Plain paragraphs. Use a blank line between paragraphs."
    )
    published = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("article_detail", kwargs={"slug": self.slug})

    def body_paragraphs(self):
        return [p.strip() for p in self.body.split("\n\n") if p.strip()]
