from django.urls import path
from book.views import BookListView, BookDetailView


app_name = "book"

urlpatterns = [
    path("books/", BookListView.as_view(), name="book-list-create"),
    path("books/<int:pk>/", BookDetailView.as_view(), name="book-detail"),
]
