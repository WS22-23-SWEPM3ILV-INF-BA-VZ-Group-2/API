# Generated by Django 4.1.3 on 2022-12-17 22:39

import uuid
from django.db import migrations, models



class Migration(migrations.Migration):

    dependencies = [
        ('unreveal', '0005_rename_username_comment_email_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.UUIDField(auto_created=True, default=uuid.uuid4, 
                editable=False, primary_key=True, serialize=False)),
                ('place_id', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=100)),
                ('rating', models.DecimalField(decimal_places=2, max_digits=5)),
            ],
        ),
    ]
