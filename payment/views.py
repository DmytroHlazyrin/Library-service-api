from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from payment.models import Payment
from payment.permissions import IsAdminOrOwner
from payment.serializers import PaymentSerializer, PaymentListSerializer
from payment.utils import create_stripe_session_for_borrowing


class PaymentListCreateView(generics.ListCreateAPIView):
    serializer_class = PaymentListSerializer
    permission_classes = (IsAuthenticated, IsAdminOrOwner)

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Payment.objects.all()
        return Payment.objects.filter(borrowing_id__user=user)

    def perform_create(self, serializer):
        payment = serializer.save()
        borrowing = payment.borrowing_id
        session = create_stripe_session_for_borrowing(borrowing)

        if session:
            payment.session_id = session.id
            payment.session_url = session.url
            payment.save()


class PaymentDetailView(generics.RetrieveAPIView):
    serializer_class = PaymentSerializer
    permission_classes = (IsAuthenticated, IsAdminOrOwner)

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Payment.objects.all()
        return Payment.objects.filter(borrowing_id__user=user)
