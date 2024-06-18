import stripe
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from botSend import send_message
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


class PaymentSuccessView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request: Request, *args, **kwargs) -> Response:
        """
        Verify payment status and update the payment record.
        """

        session_id = request.query_params.get("session_id")
        if not session_id:
            return Response(
                {"error": "No session ID provided"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            session = stripe.checkout.Session.retrieve(session_id)
            payment_intent = stripe.PaymentIntent.retrieve(
                session.payment_intent
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

        payment = get_object_or_404(Payment, session_id=session_id)
        if payment_intent.status == "succeeded":
            payment.status = Payment.PaymentStatus.PAID
            send_message(
                f"💸 Payment was successful by {self.request.user}\n"
                f"Money: {payment.money_to_pay}$"
            )
            payment.save()

        return Response(
            {
                "status": "Payment was successful",
                "payment": PaymentSerializer(payment).data,
            },
            status=status.HTTP_200_OK,
        )


class PaymentCancelView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request: Request, *args, **kwargs) -> Response:
        """
        Inform the user that the payment was canceled and can be retried later.
        """
        print("PaymentCancelView GET request called")
        return Response(
            {
                "detail": "Something went wrong! Payment can be made later. "
                "The session is available for only 24 hours."
            },
            status=status.HTTP_200_OK,
        )
