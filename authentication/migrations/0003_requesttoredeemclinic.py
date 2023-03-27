# Generated by Django 4.1.4 on 2023-03-23 20:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_remove_document_name_alter_document_file'),
    ]

    operations = [
        migrations.CreateModel(
            name='RequestToRedeemClinic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('clinic_to_redeem', models.CharField(max_length=20)),
                ('phone', models.CharField(max_length=20)),
                ('company_role', models.CharField(max_length=50)),
                ('message', models.TextField()),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]