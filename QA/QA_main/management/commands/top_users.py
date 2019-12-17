from django.core.cache import cache, caches
from django.core.management.base import BaseCommand, CommandError

from QA_main.models import Profile


def get_top_users():
	print("----------Getting top users----------")
	profiles = Profile.objects.get_top()
	tmp = list()
	for profile in profiles:
		tmp.append(profile.user.username)
	cache.set('top_users', tmp)


class Command(BaseCommand):
	def handle(self, *args, **options):
		get_top_users()
