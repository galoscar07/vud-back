# Generated by Django 4.1.4 on 2023-06-08 10:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0007_collaboratordoctor_step'),
    ]

    operations = [
        migrations.AddField(
            model_name='collaboratordoctor',
            name='is_visible',
            field=models.BooleanField(default=False),
        ),
    ]