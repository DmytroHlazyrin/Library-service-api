from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from payment.models import Payment
from payment.permissions import IsAdminOrOwner
from payment.serializers import PaymentSerializer, PaymentListSerializer


class PaymentListView(generics.ListAPIView):
    serializer_class = PaymentListSerializer
    permission_classes = (IsAuthenticated, IsAdminOrOwner)

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Payment.objects.all()
        return Payment.objects.filter(borrowing_id__user=user)


class PaymentDetailView(generics.RetrieveAPIView):
    serializer_class = PaymentSerializer
    permission_classes = (IsAuthenticated, IsAdminOrOwner)

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Payment.objects.all()
        return Payment.objects.filter(borrowing_id__user=user)
