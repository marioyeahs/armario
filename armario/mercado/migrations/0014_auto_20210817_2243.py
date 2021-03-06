# Generated by Django 3.2.5 on 2021-08-18 03:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mercado', '0013_auto_20210817_2231'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ofertas_compradas',
            name='cliente',
        ),
        migrations.RemoveField(
            model_name='ofertas_compradas',
            name='propietario',
        ),
        migrations.AddField(
            model_name='ofertas_compradas',
            name='comprador',
            field=models.ForeignKey(default=11, on_delete=django.db.models.deletion.CASCADE, related_name='comprador', to='auth.user'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ofertas_compradas',
            name='vendedor',
            field=models.ForeignKey(default=4, on_delete=django.db.models.deletion.CASCADE, to='auth.user'),
            preserve_default=False,
        ),
    ]
