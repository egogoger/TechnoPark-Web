from django.core.cache import cache, caches
from django.core.management.base import BaseCommand, CommandError

from QA_main.models import Profile, Tag


def get_top_users():
	profiles = Profile.objects.get_top()
	tmp = list()
	for profile in profiles:
		tmp.append(profile.user.username)
	cache.set('top_users', tmp)

def get_top_tags():
	tags = Tag.objects.get_top()
	tmp = list()
	for tag in tags:
		tmp.append(tag.title)
	cache.set('top_tags', tmp)

class Command(BaseCommand):
	def add_arguments(self, parser):
		parser.add_argument('--users')
		parser.add_argument('--tags')

	def handle(self, *args, **options):
		if options['users']:
			get_top_users()
		if options['tags']:
			get_top_tags()
