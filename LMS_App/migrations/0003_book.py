# Generated by Django 5.1.4 on 2024-12-07 08:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LMS_App', '0002_rename_user_library_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('author', models.CharField(max_length=255)),
                ('image', models.ImageField(upload_to='book_images/')),
                ('copies_available', models.PositiveIntegerField(default=1)),
                ('file', models.FileField(upload_to='book_files/')),
            ],
        ),
    ]