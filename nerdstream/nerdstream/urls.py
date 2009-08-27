from django.conf.urls.defaults import *

urlpatterns = patterns('',
	(r'^$', 'nerdstream.register.views.index'),															# Main Page
	(r'^create/(?P<computer_name>[^\.^/]+)/$', 'nerdstream.register.views.create_computer'),			# Create a user
	(r'^user/(?P<computer_name>[^\.^/]+)/$', 'nerdstream.register.views.user'),							# View the user details
	(r'^config/(?P<computer_name>[^\.^/]+)/$', 'nerdstream.register.views.config_user'),				# Return program config informaion
	(r'^config/(?P<computer_name>[^\.^/]+)/update/$', 'nerdstream.register.views.config_user_update'),	# Update the last flickr upload
	# (r'^user/(?P<user_key>[^\.^/]+)/results/$', 'nerdstream.register.views.user_results'),			# Display the user's images
	(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': 'nerdstream/media'}),		# Static pages
)