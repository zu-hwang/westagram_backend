# Generated by Django 3.0.5 on 2020-04-09 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_url', models.CharField(max_length=300)),
                ('description', models.CharField(max_length=100)),
                ('update_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
