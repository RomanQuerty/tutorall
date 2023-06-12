# Generated by Django 3.2.19 on 2023-06-12 07:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_appuser_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('mark', models.IntegerField()),
                ('app_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='main.appuser')),
            ],
        ),
    ]