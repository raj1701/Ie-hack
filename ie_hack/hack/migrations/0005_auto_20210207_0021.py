# Generated by Django 3.0.11 on 2021-02-07 00:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hack', '0004_auto_20210206_2354'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resource',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='resources', to='hack.Event'),
        ),
    ]
