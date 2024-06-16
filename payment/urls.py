from django.urls import path
from payment.views import (
    PaymentListView,
    PaymentDetailView,
    PaymentSuccessView,
    PaymentCancelView,
)


urlpatterns = [
    path("", PaymentListView.as_view(), name="payment-list"),
    path("<int:pk>/", PaymentDetailView.as_view(), name="payment-detail"),
    path("success/", PaymentSuccessView.as_view(), name="payment-success"),
    path("cancel/", PaymentCancelView.as_view(), name="payment-cancel"),
]

app_name = "payment"
