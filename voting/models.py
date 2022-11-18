from ordered_model.models import OrderedModel, OrderedModelManager, OrderedModelQuerySet
from polymorphic.compat import with_metaclass
from django.utils.timezone import now
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from uuid import uuid4
from django.contrib.auth.hashers import make_password
from django.utils.translation import gettext_lazy as _
from ordered_model.models import OrderedModel
from polymorphic.models import PolymorphicModel
from polymorphic.query import PolymorphicQuerySet
from polymorphic.managers import PolymorphicManager


class UserManager(BaseUserManager):

    def _create_user(self, username, password, **extra_fields):
        if not username:
            raise ValueError("The given username must be set")
        username = User.normalize_username(username)
        user = User(username=username, user_id=uuid4(), **extra_fields)
        # TODO test if empty password login is somehow possible
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


# TODO probably don't need a custom user model, just the manager
class User(AbstractBaseUser, PermissionsMixin):
    user_id = models.UUIDField(unique=True)
    is_admin = models.BooleanField(default=False)
    # TODO _most_ will be email addresses, but not the admin...
    username = models.CharField(
        _("username/email"), unique=True, max_length=255)
    USERNAME_FIELD = 'username'
    objects = UserManager()

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


class UserProfile(models.Model):
    """Model definition for UserProfile."""

    facebook_name = models.CharField(_('facebook name'), max_length=255)
    user = models.ForeignKey(User, verbose_name=_(
        "user"), on_delete=models.CASCADE)

    class Meta:
        """Meta definition for UserProfile."""

        verbose_name = 'user profile'
        verbose_name_plural = 'user profiles'

    def __str__(self):
        """Unicode representation of UserProfile."""
        return self.facebook_name


class VoteEvent(models.Model):
    class Meta:
        verbose_name = _("vote event")
        verbose_name_plural = _("vote events")

    description = models.TextField(_('event description'))
    start_at = models.DateTimeField(
        _("event start"), auto_now=False, auto_now_add=False)
    end_at = models.DateTimeField(
        _("event end"), auto_now=False, auto_now_add=False)

    def __str__(self):
        """Unicode representation of a vote event."""
        # return f'{VoteEvent._meta.verbose_name.capitalize()}: {self.description}'
        return self.description

    def has_started(self):
        return self.start_at <= now()

    def has_ended(self):
        return now() > self.end_at

    def is_live(self):
        return self.has_started() and not self.has_ended()


class ItemQuerySet(PolymorphicQuerySet, OrderedModelQuerySet):
    pass


class ItemManager(PolymorphicManager, OrderedModelManager):
    def get_queryset(self):
        return ItemQuerySet(self.model, using=self._db)


class VoteItem(PolymorphicModel, OrderedModel):
    order_class_path = __module__ + '.VoteItem'
    objects = ItemManager()

    class Meta:
        verbose_name = _("vote item")
        verbose_name_plural = _("vote items")
        ordering = ('order',)

    event = models.ForeignKey(
        VoteEvent, on_delete=models.CASCADE)
    description = models.TextField(_('description'))
    detail_link = models.URLField(_('detail link'), blank=True)

    def __str__(self):
        """Unicode representation of a vote item."""
        return self.description


class YesNoAbstain(VoteItem):
    def user_vote(self, user):
        return self.ynavote_set.filter(user=user).first()


class YNAVote(models.Model):
    class YNA(models.TextChoices):
        YES = 'Y', _('Yes')
        NO = 'N', _('No')
        ABSTAIN = 'A', _('Abstain')

    class Meta:
        unique_together = ('user', 'yna')
    choice = models.CharField(
        max_length=1, choices=YNA.choices, default=None, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    yna = models.ForeignKey(YesNoAbstain, on_delete=models.CASCADE)

    def __str__(self):
        """Unicode representation of a vote item."""
        choices = dict(self.YNA.choices)
        return str(choices[self.choice])


# class MultipleChoice(VoteItem):
#     max_votes = models.PositiveIntegerField()

#     def user_vote(self, user):
#         return None


# class ChoiceOption(models.Model):
#     item = models.ForeignKey(MultipleChoice, on_delete=models.CASCADE)
#     description = models.CharField(_('description'), max_length=255)

#     def __str__(self):
#         """Unicode representation of a choice option."""
#         return self.description


# class ChoiceVote(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     choice = models.ForeignKey(ChoiceOption, on_delete=models.CASCADE)

#     class Meta:
#         unique_together = ('user', 'choice')
