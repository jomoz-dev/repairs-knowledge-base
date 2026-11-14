from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, render

from .models import Article, Category


@login_required
def home(request):
    categories = Category.objects.all()
    recent = Article.objects.filter(published=True).order_by("-updated_at")[:6]
    return render(
        request,
        "knowledge/home.html",
        {"categories": categories, "recent": recent},
    )


@login_required
def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    articles = category.articles.filter(published=True)
    return render(
        request,
        "knowledge/category.html",
        {"category": category, "articles": articles},
    )


@login_required
def article_detail(request, slug):
    article = get_object_or_404(Article, slug=slug, published=True)
    related = (
        Article.objects.filter(published=True, category=article.category)
        .exclude(pk=article.pk)[:4]
    )
    return render(
        request,
        "knowledge/article.html",
        {"article": article, "related": related},
    )


@login_required
def search(request):
    query = request.GET.get("q", "").strip()
    results = Article.objects.none()
    if query:
        results = Article.objects.filter(published=True).filter(
            Q(title__icontains=query)
            | Q(summary__icontains=query)
            | Q(body__icontains=query)
            | Q(category__name__icontains=query)
        )
    return render(
        request,
        "knowledge/search.html",
        {"query": query, "results": results},
    )
