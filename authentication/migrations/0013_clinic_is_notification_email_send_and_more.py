# Generated by Django 4.1.4 on 2023-06-17 19:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0012_remove_clinic_collab_clinic_remove_clinic_role_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='clinic',
            name='is_notification_email_send',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='collaboratordoctor',
            name='is_notification_email_send',
            field=models.BooleanField(default=False),
        ),
    ]