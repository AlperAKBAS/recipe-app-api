from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
                                        PermissionsMixin
# Create your models here.

class UserManager(BaseUserManager):
    
    def create_user(self, email, password=None, **extra_fields):
        # password is None, maybe we add inactive users
        """Creates and saves a new user"""
        if not email:
            raise ValueError('Users must enter an email address')

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)  # We can use different database for users

        return user

    def create_superuser(self, email, password):
        """Creates and Saves a new superuser"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    # All the feature comes with the user model
    """Custom user model that supports using email instead of username"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager() 

    USERNAME_FIELD = 'email' # we converted to email default