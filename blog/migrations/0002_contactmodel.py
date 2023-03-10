# Generated by Django 4.1.4 on 2022-12-23 20:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=50)),
                ('message', models.CharField(max_length=5000)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
