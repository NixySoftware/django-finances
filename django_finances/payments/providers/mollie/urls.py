from django.urls import path

from .views import MollieWebhookView

urlpatterns = [
    path('mollie/webhook', MollieWebhookView.as_view())
]
