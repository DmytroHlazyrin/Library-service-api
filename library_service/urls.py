from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/user/", include("user.urls"), name="user"),
    path("api/book/", include("book.urls")),
    path("api/borrowing/", include("borrowing.urls")),
    path("api/payment/", include("payment.urls"), name="payment"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if not settings.TESTING:
    urlpatterns = [
        *urlpatterns,
        path("__debug__/", include("debug_toolbar.urls")),
    ]
