from django.urls import path
from payment.views import PaymentListView, PaymentDetailView


urlpatterns = [
    path('payments/', PaymentListView.as_view(), name='payment-list'),
    path('payments/<int:pk>/', PaymentDetailView.as_view(), name='payment-detail'),
]

app_name = "payment"
