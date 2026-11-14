import pytest
from django.contrib.auth.models import User
from django.urls import reverse

from knowledge.models import Article, Category


@pytest.fixture
def advisor(db):
    return User.objects.create_user(username="advisor", password="changeme")


@pytest.fixture
def article(db):
    category = Category.objects.create(
        name="Water leak",
        slug="water-leak",
        summary="Leaks and electrics.",
        typical_trades="Plumber",
        sort_order=1,
    )
    return Article.objects.create(
        category=category,
        title="Water on electrics",
        slug="water-on-electrics",
        audience=Article.AUDIENCE_ADVISOR,
        related_priority=Article.PRIORITY_EMERGENCY,
        summary="Treat as Emergency.",
        body="If water has reached sockets, send Plumber / Electrician.",
        published=True,
    )


@pytest.mark.django_db
def test_home_requires_login(client):
    response = client.get(reverse("home"))
    assert response.status_code == 302
    assert reverse("login") in response.url


@pytest.mark.django_db
def test_home_lists_categories(client, advisor, article):
    client.login(username="advisor", password="changeme")
    response = client.get(reverse("home"))
    assert response.status_code == 200
    assert b"Water leak" in response.content


@pytest.mark.django_db
def test_article_detail(client, advisor, article):
    client.login(username="advisor", password="changeme")
    response = client.get(article.get_absolute_url())
    assert response.status_code == 200
    assert b"Plumber / Electrician" in response.content
    assert b"Emergency" in response.content


@pytest.mark.django_db
def test_search_finds_article(client, advisor, article):
    client.login(username="advisor", password="changeme")
    response = client.get(reverse("search"), {"q": "sockets"})
    assert response.status_code == 200
    assert b"Water on electrics" in response.content


@pytest.mark.django_db
def test_unpublished_article_is_hidden(client, advisor, article):
    article.published = False
    article.save()
    client.login(username="advisor", password="changeme")
    response = client.get(article.get_absolute_url())
    assert response.status_code == 404


REPAIR_CATEGORIES = (
    "water-leak",
    "electrical",
    "heating",
    "damp-and-mould",
    "roofing",
    "doors-and-windows",
)


@pytest.mark.django_db
def test_seed_covers_advisor_and_resident_for_each_repair_type():
    from django.core.management import call_command

    call_command("seed_knowledge")
    for slug in REPAIR_CATEGORIES:
        articles = Article.objects.filter(category__slug=slug, published=True)
        audiences = set(articles.values_list("audience", flat=True))
        assert Article.AUDIENCE_ADVISOR in audiences, slug
        assert Article.AUDIENCE_RESIDENT in audiences, slug
    for slug in (
        "who-to-send",
        "smell-of-gas",
        "resident-smell-of-gas",
        "finding-the-stopcock",
    ):
        assert Article.objects.filter(slug=slug, published=True).exists()


@pytest.fixture
def coordinator(db):
    return User.objects.create_user(
        username="admin", password="changeme", is_staff=True
    )


@pytest.mark.django_db
def test_draft_hidden_from_advisor_visible_to_staff(client, advisor, coordinator):
    from django.core.management import call_command

    call_command("seed_knowledge")
    url = reverse("article_detail", kwargs={"slug": "out-of-hours-briefing-draft"})
    client.login(username="advisor", password="changeme")
    assert client.get(url).status_code == 404
    client.login(username="admin", password="changeme")
    response = client.get(url)
    assert response.status_code == 200
    assert b"Draft" in response.content


@pytest.mark.django_db
def test_article_shows_last_reviewed(client, advisor):
    from django.core.management import call_command

    call_command("seed_knowledge")
    client.login(username="advisor", password="changeme")
    response = client.get(
        reverse("article_detail", kwargs={"slug": "who-to-send"})
    )
    assert b"Last reviewed" in response.content
    assert b"Housing Repairs Coordinator" in response.content


@pytest.mark.django_db
def test_overdue_review_listed_for_staff_only(client, advisor, coordinator):
    from django.core.management import call_command

    call_command("seed_knowledge")
    client.login(username="advisor", password="changeme")
    home = client.get(reverse("home"))
    assert b"Review due" not in home.content
    assert b"Drafts (staff only)" not in home.content
    client.login(username="admin", password="changeme")
    staff_home = client.get(reverse("home"))
    assert b"Communal lighting on the estate" in staff_home.content
    assert b"Out-of-hours contractor briefing" in staff_home.content
