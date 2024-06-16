from django.urls import path
from book.views import BookListView, BookDetailView


app_name = "book"

urlpatterns = [
    path("", BookListView.as_view(), name="book-list-create"),
    path("<int:pk>/", BookDetailView.as_view(), name="book-detail"),
]
