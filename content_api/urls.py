from django.urls import path
from .views import KeywordListCreateView, FlagListView, FlagUpdateView, ScanContentView

urlpatterns = [
    path('keywords/', KeywordListCreateView.as_view(), name='keyword-list-create'),
    path('flags/', FlagListView.as_view(), name='flag-list'),
    path('flags/<int:pk>/', FlagUpdateView.as_view(), name='flag-update'),
    path('scan/', ScanContentView.as_view(), name='scan-content'),
]

