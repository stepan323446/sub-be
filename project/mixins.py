from rest_framework.exceptions import PermissionDenied, NotFound
from rest_framework.request import Request
from django.http import Http404

from users.models import User

class IsAuthorOrAdminSingleMixin:
    field_by_user = 'user'

    def get_object(self):
        user: User = self.request.user
        obj = super().get_object()

        if (not user.is_authenticated or getattr(obj, self.field_by_user) != user) and not user.is_superuser:
            raise PermissionDenied('You are not the author of this object')

        return obj