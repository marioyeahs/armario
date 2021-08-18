# Generated by Django 3.2.5 on 2021-08-18 03:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mercado', '0012_ofertas_compradas'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ofertas_compradas',
            name='comprador',
        ),
        migrations.AddField(
            model_name='ofertas_compradas',
            name='cliente',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='comprador', to='auth.user'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ofertas_compradas',
            name='propietario',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='auth.user'),
            preserve_default=False,
        ),
    ]
