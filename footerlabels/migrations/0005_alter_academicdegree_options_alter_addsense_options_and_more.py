# Generated by Django 4.1.4 on 2023-06-11 12:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('footerlabels', '0004_delete_collaboratordoctor'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='academicdegree',
            options={'verbose_name': 'Grad Medical', 'verbose_name_plural': 'Grade Medicale'},
        ),
        migrations.AlterModelOptions(
            name='addsense',
            options={'verbose_name': 'Add Sense', 'verbose_name_plural': 'Add-uri Sense'},
        ),
        migrations.AlterField(
            model_name='blogpost',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='blogposts', to='footerlabels.tag'),
        ),
    ]