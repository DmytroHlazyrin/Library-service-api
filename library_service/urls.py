from django.conf import settings
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/user/", include("user.urls"), name="user"),
    path("api/book/", include("book.urls")),
    path("api/borrowing/", include("borrowing.urls")),
    path("api/payment/", include("payment.urls"), name="payment"),
]

if not settings.TESTING:
    urlpatterns = [
        *urlpatterns,
        path("__debug__/", include("debug_toolbar.urls")),
    ]
