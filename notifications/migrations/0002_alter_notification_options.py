# Generated by Django 4.1.7 on 2023-03-12 06:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='notification',
            options={'ordering': ['-created_at'], 'verbose_name': 'notification', 'verbose_name_plural': 'notifications'},
        ),
    ]