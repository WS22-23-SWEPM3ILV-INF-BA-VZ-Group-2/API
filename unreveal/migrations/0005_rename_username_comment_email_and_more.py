# Generated by Django 4.1.3 on 2022-12-16 23:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('unreveal', '0004_rename_place_place_name_alter_comment_id_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='username',
            new_name='email',
        ),
        migrations.RenameField(
            model_name='place',
            old_name='username',
            new_name='email',
        ),
    ]
