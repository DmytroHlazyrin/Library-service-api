from django.contrib import admin
from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "payment_type",
        "status",
        "borrowing_id",
        "money_to_pay",
        "session_url",
        "session_id",
    )
    list_filter = ("status", "payment_type")
    search_fields = ("borrowing_id", "session_id")
