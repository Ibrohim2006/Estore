from django.db import models
from .utils import phone_number_validation

Status = (
    (1, 'Sent_to_check'),
    (2, 'In_progress'),
    (3, 'Checked')

)


class ContactModel(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=13, validators=[phone_number_validation])
    message = models.TextField()

    status = models.IntegerField(choices=Status, default=1)
    is_solved = models.BooleanField(default=False)

    delete_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.full_name}::{self.phone_number}"

    class Meta:
        db_table = 'contact'
        verbose_name = 'Contact'
        verbose_name_plural = 'Contacts'

class AboutModel(models.Model):
    location = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=13, validators=[phone_number_validation])
    email = models.EmailField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email

    class Meta:
        db_table = 'about'
        verbose_name = 'About'
        verbose_name_plural = 'Abouts'
