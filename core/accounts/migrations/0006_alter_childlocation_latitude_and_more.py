# Generated by Django 4.2.7 on 2023-11-04 08:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_child_unique_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='childlocation',
            name='latitude',
            field=models.DecimalField(decimal_places=6, max_digits=9),
        ),
        migrations.AlterField(
            model_name='childlocation',
            name='latitudeDelta',
            field=models.DecimalField(decimal_places=6, max_digits=9),
        ),
        migrations.AlterField(
            model_name='childlocation',
            name='longitude',
            field=models.DecimalField(decimal_places=6, max_digits=9),
        ),
        migrations.AlterField(
            model_name='childlocation',
            name='longitudeDelta',
            field=models.DecimalField(decimal_places=6, max_digits=9),
        ),
    ]