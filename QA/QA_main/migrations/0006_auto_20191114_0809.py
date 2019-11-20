# Generated by Django 2.2.5 on 2019-11-14 08:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('QA_main', '0005_auto_20191105_1546'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='answer',
            options={'ordering': ['-correctness', '-datetime'], 'verbose_name': 'Ответ', 'verbose_name_plural': 'Ответы'},
        ),
        migrations.RemoveField(
            model_name='answer',
            name='rating',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='disliked_answers',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='disliked_questions',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='liked_answers',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='liked_questions',
        ),
        migrations.RemoveField(
            model_name='question',
            name='slug',
        ),
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(default='static/images/avatars/crowd.jpg', upload_to='static/images/avatars/'),
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('liked', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='liked', to='QA_main.Question')),
                ('liker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='liker', to='QA_main.Profile')),
            ],
            options={
                'verbose_name': 'Лайк',
                'verbose_name_plural': 'Лайки',
                'unique_together': {('liker', 'liked')},
            },
        ),
    ]