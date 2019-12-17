import os
import django
import random
from datetime import datetime
from django.contrib.auth.models import User
from QA_main.models import Profile, Question, Answer, Tag, Like
from faker.providers.person.en import Provider
from faker import Faker
from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ObjectDoesNotExist



os.environ.setdefault('DJANGO_SETTINGS_MODULE','server_engine.settings')
django.setup()
fake = Faker()

def generate_users(user_size):
    path = 'uploads/avatars/'
    usernames = list(set(Provider.first_names))
    random.seed(datetime.now())
    random.shuffle(usernames)
    i = 0
    shuffled = 1
    while i < user_size:
        try:
            username = usernames[i] + str(shuffled)
            email = fake.email()
            
            # this part is picking random avatars from folder
            avatar = random.choice([
                x for x in os.listdir(path)
                if os.path.isfile(os.path.join(path, x))])
            if avatar == '.DS_Store':
                avatar = 'crowd.jpg'
            avatar = 'avatars/' + avatar
            
            user = User.objects.create(username=username, email=email, password="password")
            Profile.objects.create(user=user, avatar=avatar)
            i += 1
        except IndexError:      # because list of names isn't holeless
            user_size = user_size - i
            i = 0
            shuffled += 1
        
def generate_tags(tags_size):
    tags = list(Tag.objects.all())
    for i in range(tags_size):
        title = fake.text()[0:10].replace(" ", "")
        while title in tags:
            title = fake.text()[0:10].replace(" ", "")
        tags.append(title)
        Tag.objects.create(title=title)

def generate_questions(questions_size):
    max_p = Profile.objects.all().order_by("-pk")[0].pk
    min_p = Profile.objects.all().order_by("pk")[0].pk
    max_t = Tag.objects.all().order_by("-pk")[0].pk
    min_t = Tag.objects.all().order_by("pk")[0].pk
    i = 0;
    while i < questions_size:
        profile_id = random.randint(min_p, max_p)
        try:
            author = Profile.objects.get(pk=profile_id)
            title = fake.text()[0:20]
            body = fake.text()[0:300]
            rating = random.randint(0, 500)
            tags = []
            for j in range(3):
                tmp = Tag.objects.get(pk=random.randint(min_t, max_t))
                while tmp in tags:
                    tmp = Tag.objects.get(pk=random.randint(min_t, max_t))
                tags.append(tmp)
            q = Question.objects.create(title=title, body=body, author=author, rating=rating)
            q.tags.set(tags)
            i += 1
        except ObjectDoesNotExist:
            pass

def generate_answers(answers_size):
    max_p = Profile.objects.all().order_by("-pk")[0].pk
    min_p = Profile.objects.all().order_by("pk")[0].pk
    max_q = Question.objects.all().order_by("-pk")[0].pk
    min_q = Question.objects.all().order_by("pk")[0].pk
    i = 0
    while i < answers_size:
        try:
            author = Profile.objects.get(pk=random.randint(min_p, max_p))
            body = fake.text()[0:300]
            questions = Question.objects.get(pk=random.randint(min_q, max_q))
            correctness = random.choice((False, True))
            Answer.objects.create(body=body, author=author, correctness=correctness, questions=questions)
            i += 1
        except ObjectDoesNotExist:
            pass


def generate_likes(likes_size):
    max_p = Profile.objects.all().order_by("-pk")[0].pk
    min_p = Profile.objects.all().order_by("pk")[0].pk
    max_q = Question.objects.all().order_by("-pk")[0].pk
    min_q = Question.objects.all().order_by("pk")[0].pk
    i = 0
    while i < likes_size:
        author = Profile.objects.get(pk=random.randint(min_p, max_p))
        question = Question.objects.get(pk=random.randint(min_q, max_q))
        if not Like.objects.filter(liker=author, liked=question).exists():
            Like.objects.create(liker=author, liked=question)
            i += 1


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--users', type=int)
        parser.add_argument('--questions', type=int)
        parser.add_argument('--answers', type=int)
        parser.add_argument('--tags', type=int)
        parser.add_argument('--likes', type=int)

    def handle(self, *args, **options):
        if options['users']:
            print("Generating users", options['users'])
            generate_users(options['users'])
        if options['questions']:
            print("Generating questions", options['questions'])
            generate_questions(options['questions'])
        if options['answers']:
            print("Generating answers", options['answers'])
            generate_answers(options['answers'])
        if options['tags']:
            print("Generating tags", options['tags'])
            generate_tags(options['tags'])
        if options['likes']:
            print("Generating likes", options['likes'])
            generate_likes(options['likes'])
