# Generated by Django 4.1.4 on 2023-06-08 10:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0006_alter_collaboratordoctor_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='collaboratordoctor',
            name='step',
            field=models.CharField(default=0, max_length=2),
        ),
    ]
