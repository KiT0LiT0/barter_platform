# Generated by Django 5.2.1 on 2025-05-18 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ads', '0002_alter_exchangeproposal_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ad',
            name='category',
            field=models.CharField(choices=[('Книги', 'Книги'), ('Электроника', 'Электроника'), ('Одежда', 'Одежда')], max_length=100),
        ),
        migrations.AlterField(
            model_name='ad',
            name='condition',
            field=models.CharField(choices=[('новое', 'Новое'), ('б/у', 'Б/у')], max_length=50),
        ),
    ]
