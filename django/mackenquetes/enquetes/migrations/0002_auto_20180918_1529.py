# Generated by Django 2.1 on 2018-09-18 18:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('enquetes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='escolha',
            name='votos',
            field=models.IntegerField(default=0),
        ),
    ]
