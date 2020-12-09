import random

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class CustomUserManager(BaseUserManager):
    def _create_user(self, username, email, password, **extra_fields):
        if username == "":
            username = "{}-{}".format(
                self.email.split("@")[0], random.randint(11111111, 99999999)
            )
        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(username, email, password, **extra_fields)

    def available(self):
        return self.filter(is_deleted=False)


class CustomUser(AbstractBaseUser):
    username = models.CharField(max_length=50, unique=True, blank=True)
    name = models.CharField(max_length=150)
    surname = models.CharField(max_length=150)
    docid = models.CharField(max_length=11, unique=True)
    email = models.EmailField(max_length=150, unique=True)
    photo_url = models.CharField(max_length=150)

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = "username"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["name", "email"]

    def clean(self):
        super().clean()
        self.docid = self.docid.replace('-', '')
        self.docid = self.docid.replace('.', '')
        self.docid = self.docid.strip()
        self.email = self.__class__.objects.normalize_email(self.email)


@receiver(post_save, sender=CustomUser)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)