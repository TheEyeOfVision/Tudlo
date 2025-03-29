# summarization_project/urls.py

from django.contrib import admin
from django.urls import path
from .views import home, summarize_view  # removed upload_summarize_view

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home, name="home"),
    path("summarize/", summarize_view, name="summarize"),  # single endpoint
]
