# Generated by Django 2.2.7 on 2019-12-18 07:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('QA_main', '0009_auto_20191217_0713'),
    ]

    operations = [
        migrations.AddField(
            model_name='tag',
            name='rating',
            field=models.IntegerField(default=0, verbose_name='Рейтинг'),
        ),
    ]
