from django.db.models import QuerySet
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from user.schemas import (
    create_user_view_schema,
    manage_user_view_schema,
    token_obtain_pair_schema,
    token_refresh_schema,
    token_verify_schema,
)

from user.serializers import UserSerializer


@create_user_view_schema
class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer


@manage_user_view_schema
class ManageUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self) -> QuerySet:
        return self.request.user
