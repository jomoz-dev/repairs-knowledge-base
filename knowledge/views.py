from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404, render

from .models import Article, Category


def visible_articles(user):
    articles = Article.objects.all()
    if user.is_staff:
        return articles
    return articles.filter(published=True)


@login_required
def home(request):
    categories = Category.objects.all()
    recent = (
        visible_articles(request.user)
        .filter(published=True)
        .order_by("-updated_at")[:6]
    )
    drafts = Article.objects.none()
    review_due = Article.objects.none()
    if request.user.is_staff:
        drafts = Article.objects.filter(published=False)
        review_due = [
            article
            for article in Article.objects.filter(published=True)
            if article.review_is_due()
        ]
    return render(
        request,
        "knowledge/home.html",
        {
            "categories": categories,
            "recent": recent,
            "drafts": drafts,
            "review_due": review_due,
        },
    )


@login_required
def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    articles = visible_articles(request.user).filter(category=category)
    return render(
        request,
        "knowledge/category.html",
        {"category": category, "articles": articles},
    )


@login_required
def article_detail(request, slug):
    article = get_object_or_404(Article, slug=slug)
    if not article.published and not request.user.is_staff:
        raise Http404()
    related = (
        visible_articles(request.user)
        .filter(category=article.category)
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
        results = visible_articles(request.user).filter(
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
