# Generated by Django 4.1.3 on 2023-03-09 03:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('pictures', '0003_rename_upload_file_comment_target'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]



# Generated by Django 4.1.3 on 2023-03-09 03:56

# from django.conf import settings
# from django.db import migrations, models
# import django.db.models.deletion
#
#
# class Migration(migrations.Migration):
#
#     dependencies = [
#         ('pictures', '0003_rename_upload_file_comment_target'),
#     ]
#
#     operations = [
#         migrations.AddField(
#             model_name='comment',
#             name='user',
#             field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
#         ),
#     ]