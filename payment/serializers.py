from rest_framework import serializers

from payment.models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = [
            "id",
            "status",
            "payment_type",
            "borrowing_id",
            "session_url",
            "session_id",
            "money_to_pay"
        ]


class PaymentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ["id", "status", "payment_type", "money_to_pay", "session_url"]
