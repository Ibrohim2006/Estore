# Generated by Django 5.1 on 2024-12-12 11:23

import contact.utils
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0004_remove_profilemodel_age'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profilemodel',
            name='address',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='address'),
        ),
        migrations.AlterField(
            model_name='profilemodel',
            name='city',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='city'),
        ),
        migrations.AlterField(
            model_name='profilemodel',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='created at'),
        ),
        migrations.AlterField(
            model_name='profilemodel',
            name='date_of_birth',
            field=models.DateField(blank=True, null=True, verbose_name='date of birth'),
        ),
        migrations.AlterField(
            model_name='profilemodel',
            name='first_name',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='first name'),
        ),
        migrations.AlterField(
            model_name='profilemodel',
            name='gender',
            field=models.PositiveSmallIntegerField(choices=[(1, '----'), (2, 'Male'), (3, 'Female')], default=1, verbose_name='gender'),
        ),
        migrations.AlterField(
            model_name='profilemodel',
            name='last_name',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='last name'),
        ),
        migrations.AlterField(
            model_name='profilemodel',
            name='phone_number',
            field=models.CharField(max_length=13, validators=[contact.utils.phone_number_validation], verbose_name='phone number'),
        ),
        migrations.AlterField(
            model_name='profilemodel',
            name='profile_picture',
            field=models.ImageField(default='img/default_user_image.png', upload_to='profile_pictures', verbose_name='profile picture'),
        ),
        migrations.AlterField(
            model_name='profilemodel',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='updated at'),
        ),
        migrations.AlterField(
            model_name='usermodel',
            name='email',
            field=models.EmailField(max_length=254, unique=True, verbose_name='email'),
        ),
    ]
