# Generated by Django 4.1.3 on 2023-02-24 03:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pictures', '0002_comment'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='upload_file',
            new_name='target',
        ),
    ]
