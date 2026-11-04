from django.urls import path

from . import views


urlpatterns = [
    path("content/", views.site_content, name="site-content"),
    path("products/", views.products, name="products"),
    path("contact/", views.contact, name="contact"),
]