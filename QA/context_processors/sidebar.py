from django.template.context_processors import request

from QA_main.models import *
 
def sidebar(request):
	tags = Tag.objects.all()
	users = User.objects.all()
	return {'sidebar_tags': tags, 'sidebar_users': users}