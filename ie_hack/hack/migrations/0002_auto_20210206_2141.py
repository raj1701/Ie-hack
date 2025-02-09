# Generated by Django 3.0.11 on 2021-02-06 21:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('hack', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='active',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='Resource',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('link', models.TextField()),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hack.Event')),
            ],
        ),
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('status', models.IntegerField(choices=[(0, 'Pending'), (1, 'Accepted'), (-1, 'Rejected')], default=0)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
