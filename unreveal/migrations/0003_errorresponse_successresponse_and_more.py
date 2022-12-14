# Generated by Django 4.1.3 on 2022-12-16 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('unreveal', '0002_rename_user_id_place_username'),
    ]

    operations = [
        migrations.CreateModel(
            name='ErrorResponse',
            fields=[
                ('id', models.BigAutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('error', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='SuccessResponse',
            fields=[
                ('id', models.BigAutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=200)),
            ],
        ),
        migrations.RenameField(
            model_name='comment',
            old_name='post_id',
            new_name='place_id',
        ),
        migrations.RenameField(
            model_name='comment',
            old_name='sender_id',
            new_name='username',
        ),
    ]
