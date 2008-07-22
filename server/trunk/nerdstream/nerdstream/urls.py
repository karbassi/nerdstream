from django.conf.urls.defaults import *

urlpatterns = patterns('',
	(r'^$', 'nerdstream.register.views.index'),
	# (r'^create/$', 'nerdstream.register.views.create'),
	(r'^create/(?P<computer_name>[^\.^/]+)/$', 'nerdstream.register.views.create_computer'),
	# (r'^user/(?P<user_key>[^\.^/]+)/$', 'nerdstream.register.views.user_details'),
	# (r'^user/(?P<user_key>[^\.^/]+)/results/$', 'nerdstream.register.views.user_results'),
	(r'^user/(?P<computer_name>[^\.^/]+)/config/$', 'nerdstream.register.views.user_config'),
	(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': 'nerdstream/media'}),
)