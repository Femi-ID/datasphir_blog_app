from django.db import models
from django.contrib.auth.models import User, AbstractUser, PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
import uuid
from .enums import GenderChoice


class CustomUserManager(BaseUserManager):
    def create_user(self, password, **extra_fields): # email, user_type,
        # **extra_fields are the fields that come with the default django user model
        # if not email:
        #     raise ValueError("Email must be provided!!")
        if not password:
            raise ValueError("Password must be provided!!")
        
        # to create the user object
        user = self.model(
            # email=self.normalize_email(email),
            # first_name=first_name,
            # last_name=last_name,
            **extra_fields)

        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, password, **extra_fields):
        # other fields:  first_name, last_name
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser is_staff must be 'True'")
        
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser is_superuser must be 'True'")

        if extra_fields.get("is_active") is not True:
            raise ValueError("Superuser is_active must be 'True'")

        return self.create_user(password=password,
                                # email=email, 
                                **extra_fields)


class User(AbstractUser, PermissionsMixin):
    # std_user = models.OneToOneField(User, null=False, on_delete=models.CASCADE)
    id = models.UUIDField(default=uuid.uuid4,  primary_key=True, editable=False, unique=True)
    username = models.CharField(max_length=250, unique=True, null=True, blank=True)
    email = models.EmailField(max_length=250, unique=True)
    phone_number = models.CharField(max_length=15, unique=True, null=True, blank=True)
    # profile_picture = models.ImageField()
    gender = models.CharField(max_length=8, choices=GenderChoice, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # create UserManager object to use this custom model.
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['password']

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Username: {self.username} >> email: {self.email}"


