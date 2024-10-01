from django.urls import path
from django.urls import path
from .views import (
    PhishingLinkCreateView,
    PhishingLinkDetailView,
    PhishingDataCreateView,
    PhishingDataListView
)

urlpatterns = [
    # URL pattern for creating a new phishing link
    path('phishing-links/', PhishingLinkCreateView.as_view(), name='phishing-link-create'),

    # URL pattern for getting and deleting a specific phishing link by ID
    path('phishing-links/<int:pk>/', PhishingLinkDetailView.as_view(), name='phishing-link-detail'),

    # URL pattern for creating new phishing data
    path('phishing-data/', PhishingDataCreateView.as_view(), name='phishing-data-create'),

    # URL pattern for listing all phishing data
    path('phishing-data/list/', PhishingDataListView.as_view(), name='phishing-data-list'),
]
