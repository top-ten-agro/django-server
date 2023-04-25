# Generated by Django 4.2 on 2023-04-25 16:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='storerole',
            name='employee',
        ),
        migrations.AddField(
            model_name='storerole',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='store',
            name='employees',
            field=models.ManyToManyField(related_name='stores', through='store.StoreRole', to=settings.AUTH_USER_MODEL),
        ),
    ]
