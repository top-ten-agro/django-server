# Generated by Django 4.2 on 2023-05-19 06:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_alter_storerole_store_alter_storerole_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='balance',
            name='officer',
            field=models.ForeignKey(blank=True, limit_choices_to={models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='balances', to='store.store'): models.F('store')}, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='officers', to='store.storerole'),
        ),
    ]
