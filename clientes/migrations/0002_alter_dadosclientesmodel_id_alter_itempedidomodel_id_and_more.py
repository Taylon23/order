# Generated by Django 4.2.6 on 2023-10-19 11:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clientes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dadosclientesmodel',
            name='id',
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='itempedidomodel',
            name='id',
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='pedidomodel',
            name='id',
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
    ]