from django.core.cache import cache, caches
from django.template.context_processors import request

from QA_main.models import *
 
def sidebar(request):
	tags = cache.get('top_tags')
	if not tags:
		tags = Tag.objects.all()[:10]
	profiles = cache.get('top_users')
	if not profiles:
		profiles = Profile.objects.all()[:10]
	return {'sidebar_tags': tags, 'sidebar_users': profiles}