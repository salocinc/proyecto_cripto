# Generated by Django 4.2 on 2023-07-16 18:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_inicial', '0004_document'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='file_txt',
            field=models.FileField(blank=True, null=True, upload_to='static/texts/'),
        ),
    ]
