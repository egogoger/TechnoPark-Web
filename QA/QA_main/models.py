# coding=utf-8
from django.db import models
from django.contrib.auth.models import User


class ProfileManager(models.Manager):
    def save(self, cleaned_data, image):
        user = User.objects.create_user(
                            username=cleaned_data['username'],
                            password=cleaned_data['password1'])
        if cleaned_data['email']:
            user.email = cleaned_data['email']

        self.create(user=user,
                    avatar=image,
                    date=cleaned_data['date'])

    def get_top(self):
        return self.order_by('-rating')[:10]


class Profile(models.Model):
    user      = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar    = models.ImageField(blank=True, upload_to='avatars/',
                                  default='uploads/avatars/crowd.jpg')
    date      = models.DateField(null=True, verbose_name='День Рождения')
    rating    = models.IntegerField(default=0)

    objects   = ProfileManager()

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'
        ordering = ['-rating']


class QuestionManager(models.Manager):
    def show_new(self):
        return self.order_by('-datetime_published')

    def show_top(self):
        return self.order_by('-rating')

    def show_users(self, author):
        return self.filter(author=author).order_by('-rating')

    def save(self, object_list, user):
        q = self.create(title=object_list['title'],
                        body=object_list['body'],
                        author=user)
        q.tags.set(object_list['tags'])


class Question(models.Model):
    title     = models.CharField(max_length=255, verbose_name='Заголовок')
    body      = models.TextField(blank=True, verbose_name='Текст')
    author    = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='questions')
    datetime_published = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    rating    = models.IntegerField(default=0, verbose_name='Рейтинг')

    tags      = models.ManyToManyField('Tag',
                                    blank=True,
                                    related_name='questions',
                                    verbose_name='Теги')
    objects   = QuestionManager()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'
        ordering = ['-datetime_published']
        unique_together = [('title'), ('body')]


class Answer(models.Model):
    body          = models.TextField(null=True, verbose_name='Текст')
    author        = models.ForeignKey(Profile, on_delete=models.CASCADE)
    datetime      = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    correctness   = models.BooleanField(default=False, verbose_name='Правильность')
    questions     = models.ForeignKey(Question,
                                    null=True,
                                    related_name='answers',
                                    verbose_name='Вопросы',
                                    on_delete=models.CASCADE)

    def __str__(self):
        return str(self.author) + " ANSWERED " + str(self.questions)

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'
        ordering = ['-correctness', '-datetime']


class TagManager(models.Manager):
    def get_top(self):
        return self.order_by('-rating')[:10]


class Tag(models.Model):
    title = models.CharField(max_length=50, unique=True)
    rating = models.IntegerField(default=0, verbose_name='Рейтинг')

    objects = TagManager()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ['title']


class Like(models.Model):
    liker = models.ForeignKey(Profile, related_name='liker', on_delete=models.CASCADE)
    liked = models.ForeignKey(Question, related_name='liked', on_delete=models.CASCADE)
    value = models.SmallIntegerField(default=0, verbose_name='Значение')

    def __str__(self):
        return str(self.liker) + " LIKED " + str(self.liked)

    class Meta:
        verbose_name = 'Лайк'
        verbose_name_plural = 'Лайки'
        unique_together = [('liker'),('liked')]

