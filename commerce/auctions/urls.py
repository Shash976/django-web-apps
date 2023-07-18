from django.urls import path, re_path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .models import *


listings = f"({('|').join([str(listing.id) for listing in Listing.objects.all()])})"
categories = f"({('|').join([category.category for category in Category.objects.all()])})"
users = f"({('|').join([user.username for user in User.objects.all()])})"

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create_listing, name="create"),
    path("categories", views.categories, name="categories"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("<int:listing_id>", views.listing, name="listing"),
    re_path(categories, views.category, name="category"),
    re_path(users, views.person_listings, name="person_listings")
]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)
