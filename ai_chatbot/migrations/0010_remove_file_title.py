# Generated by Django 4.2.1 on 2023-08-18 09:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ai_chatbot', '0009_file'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='file',
            name='title',
        ),
    ]
