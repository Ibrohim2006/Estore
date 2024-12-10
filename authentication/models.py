from django.db import models
from django.contrib.auth.models import AbstractUser
from contact.utils import phone_number_validation
from .managers import CustomUserManager
from datetime import date

Gender_choices = (
    (1, '----'),
    (2, 'Male'),
    (3, 'Female'),
)


class UserModel(AbstractUser):
    username = None
    email = models.EmailField(unique=True, null=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        db_table = 'user'


class ProfileModel(models.Model):
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50,  null=True, blank=True)
    gender = models.PositiveSmallIntegerField(choices=Gender_choices, default=1)
    phone_number = models.CharField(max_length=13, validators=[phone_number_validation])
    profile_picture = models.ImageField(upload_to='profile_pictures', default='img/default_user_image.png')
    date_of_birth = models.DateField(null=True, blank=True)
    city = models.CharField(max_length=30, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def calculate_age(self):
        if not self.date_of_birth:
            return None
        today = date.today()
        return today.year - self.date_of_birth.year - (
                (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))

    def __str__(self):
        return self.user.email

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'
        db_table = 'profile'