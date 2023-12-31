from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import UserManager
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractBaseUser, PermissionsMixin):
    # AbstractBaseUser
    username = models.CharField(_('username'), max_length=150)
    email = models.EmailField(_('email address'), unique=True)
    age = models.PositiveIntegerField(('Age'), default=0, blank=True)
    # PermissionsMixin
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(_('staff status'), default=False)
    is_active = models.BooleanField(_('active'), default=True)
    data_joined = models.DateTimeField(_('data joined'), default=timezone.now)
    # PermissionsMixin
    objects = UserManager()
    # AbstractBaseUser
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    # AbstractBaseUser
    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        db_table = 'users'
        swappable = 'AUTH_USER_MODEL'
        # basado en BaseUser
    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)
        # basado en BaseUser
    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)
