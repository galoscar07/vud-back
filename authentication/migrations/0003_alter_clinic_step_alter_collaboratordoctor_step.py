# Generated by Django 4.1.4 on 2024-02-20 22:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_import_clinics'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clinic',
            name='step',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='collaboratordoctor',
            name='step',
            field=models.IntegerField(default=0),
        ),
    ]
