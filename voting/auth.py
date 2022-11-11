from typing import Any, Optional

from django.contrib.auth.backends import AllowAllUsersModelBackend
from django.http import HttpRequest

from voting.models import User


class AuthBackend(AllowAllUsersModelBackend):
    def authenticate(self, request: Optional[HttpRequest], user_id: Optional[str] = None, **kwargs) -> Optional[User]:
        # return super().authenticate(request, username, password, **kwargs)
        if user_id is not None:
            return User.objects.get(user_id=user_id)
        else:
            return super().authenticate(request, username=None, password=kwargs.get('password'), **kwargs)
