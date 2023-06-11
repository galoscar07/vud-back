# Generated by Django 4.1.4 on 2023-06-08 12:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0008_collaboratordoctor_is_visible'),
    ]

    operations = [
        migrations.CreateModel(
            name='DoctorReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.PositiveIntegerField()),
                ('comment', models.TextField(blank=True)),
                ('name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('is_visible', models.BooleanField(default=False)),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='authentication.collaboratordoctor')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]
