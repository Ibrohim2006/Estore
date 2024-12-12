from django.db import models
from .utils import phone_number_validation
from django.utils.translation import gettext_lazy as _

Status = (
    (1, 'Sent_to_check'),
    (2, 'In_progress'),
    (3, 'Checked')

)


class ContactModel(models.Model):
    full_name = models.CharField(_("full name"), max_length=100)
    email = models.EmailField(_("email"))
    phone_number = models.CharField(_("phone number"), max_length=13, validators=[phone_number_validation])
    message = models.TextField(_("message"))

    status = models.IntegerField(_("status"), choices=Status, default=1)
    is_solved = models.BooleanField(_("is solved"), default=False)

    delete_at = models.DateTimeField(_("deleted at"), null=True, blank=True)
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)

    def __str__(self):
        return f"{self.full_name}::{self.phone_number}"

    class Meta:
        db_table = 'contact'
        verbose_name = _("Contact")
        verbose_name_plural = _("Contacts")

class AboutModel(models.Model):
    location = models.CharField(_("location"), max_length=150)
    phone_number = models.CharField(_("phone number"), max_length=13, validators=[phone_number_validation])
    email = models.EmailField(_("email"))

    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)

    def __str__(self):
        return self.email

    class Meta:
        db_table = 'about'
        verbose_name = _("About")
        verbose_name_plural = _("Abouts")
