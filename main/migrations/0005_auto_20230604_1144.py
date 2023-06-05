# Generated by Django 3.2.19 on 2023-06-04 11:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20230518_1602'),
    ]

    operations = [
        migrations.AddField(
            model_name='scheduletablecell',
            name='reserved_by',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reserved_by', to='main.appuser'),
        ),
        migrations.AlterField(
            model_name='scheduletablecell',
            name='teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='teacher', to='main.appuser'),
        ),
    ]