from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from uuid import uuid4
from django.contrib.auth.hashers import make_password


class UserManager(BaseUserManager):

    def _create_user(self, username, password, **extra_fields):
        if not username:
            raise ValueError("The given username must be set")
        username = User.normalize_username(username)
        user = User(username=username, user_id=uuid4(), **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, password=None, **extra_fields):
        extra_fields.setdefault("is_superuser", False)

        return self._create_user(username, password, **extra_fields)

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(username, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    user_id = models.UUIDField(unique=True)
    # TODO _most_ will be email addresses, but not the admin...
    username = models.CharField(unique=True, max_length=254)
    USERNAME_FIELD = 'username'
    objects = UserManager()
