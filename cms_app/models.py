from django.db import models
from rest_framework.authtoken.models import Token
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings


class UserManager(BaseUserManager):
    def create_user(self, email, full_name, phone, password):
        if not email:
            raise ValueError("user must have an email address!")
        if not full_name:
            raise ValueError("user must have their full name!")
        if not phone:
            raise ValueError("user must have a phone number!")
        user = self.model(
            email = self.normalize_email(email),
            full_name = full_name,
            phone = phone
        )
        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_superuser(self, email, full_name, phone, password):
        user = self.create_user(
            email = self.normalize_email(email),
            full_name = full_name,
            phone=phone,
            password=password,
        )
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class UserRegister(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=50)
    full_name = models.CharField(max_length=100)
    phone = models.CharField(
        max_length=10,
        validators=[
            RegexValidator(
            regex=r'^\d[0-9]{9,10}$',
            message="Phone number must be entered in the format '1234567890'. Up to 10 digits allowed."
            ),
        ],
    )
    address = models.TextField(blank=True)
    city = models.CharField(max_length=20, blank=True)
    state = models.CharField(max_length=30, blank=True)
    country = models.CharField(max_length=50, blank=True)
    pincode = models.CharField(
        max_length=6,
        validators=[
            RegexValidator(
            regex=r'^\d[0-9]{4,6}$',
            message="Pincode must be entered in the format '123456'. Up to 6 digits allowed."
            ),
        ],
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name', 'phone']

    def __str__(self):
        return self.email


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class ContentItem(models.Model):
    user=models.ForeignKey(UserRegister, on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    body = models.CharField(max_length=300)
    summary = models.CharField(max_length=60)
    document = models.FileField(upload_to='cms_app/pdf_document/%Y/%m/%d')
    category = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.title