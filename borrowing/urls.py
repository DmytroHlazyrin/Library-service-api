from django.urls import path

from borrowing.views import (
    BorrowingListCreateAPIView,
    BorrowingDetailAPIView,
    return_borrowing,
)

urlpatterns = [
    path(
        "", BorrowingListCreateAPIView.as_view(), name="borrowing-list-create"
    ),
    path(
        "<int:pk>/", BorrowingDetailAPIView.as_view(), name="borrowing-detail"
    ),
    path(
        "<int:pk>/return/", return_borrowing, name="return-borrowing"
    ),
]
