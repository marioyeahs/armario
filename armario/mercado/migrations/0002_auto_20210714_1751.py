# Generated by Django 3.2.5 on 2021-07-14 22:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mercado', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='mercancia',
            name='depto',
            field=models.CharField(choices=[('CZ', 'Calzado'), ('RP', 'Ropa'), ('JG', 'Juguete'), ('CL', 'Coleccionable')], default='Cz', max_length=2),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='mercancia',
            name='size_type',
            field=models.CharField(choices=[('M', 'Men'), ('W', 'Women'), ('CH', 'Child'), ('PS', 'Preschool'), ('IF', 'Infant'), ('TD', 'Toddler')], default='PS', max_length=2),
            preserve_default=False,
        ),
    ]
