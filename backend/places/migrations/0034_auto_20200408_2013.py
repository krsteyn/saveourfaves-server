# Generated by Django 3.0.4 on 2020-04-08 20:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0033_submittedplace_donation_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='place',
            name='phone_number',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='submittedplace',
            name='phone_number',
            field=models.TextField(blank=True, null=True),
        ),
    ]
