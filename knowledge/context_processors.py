from .models import Category


def nav_categories(request):
    if not request.user.is_authenticated:
        return {"nav_categories": []}
    return {"nav_categories": Category.objects.all()}
