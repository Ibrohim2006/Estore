# Generated by Django 5.1 on 2024-12-09 08:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='productmodel',
            name='deal_end_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='productmodel',
            name='deal_start_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='productmodel',
            name='month_of_deal',
            field=models.BooleanField(default=False),
        ),
    ]