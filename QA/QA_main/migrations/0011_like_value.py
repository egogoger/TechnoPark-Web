# Generated by Django 2.2.7 on 2019-12-18 08:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('QA_main', '0010_tag_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='like',
            name='value',
            field=models.SmallIntegerField(default=0, verbose_name='Значение'),
        ),
    ]
