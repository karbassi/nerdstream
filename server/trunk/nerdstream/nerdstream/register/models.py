from google.appengine.ext import db

class Users(db.Model):
	full_name = db.StringProperty()
	computer_name = db.StringProperty()
	job_title = db.StringProperty(default='Programmer')
	start_time = db.IntegerProperty(default=800)
	end_time = db.IntegerProperty(default=1700)
	interval = db.IntegerProperty(default=5)
	last_update = db.DateTimeProperty(auto_now=1)
	creation_date = db.DateTimeProperty(auto_now_add=1)
	
	def __str__(self):
		return '%s' %self.computer_name
	
	def get_absolute_url(self):
		# return '/user/%s/config' % self.computer_name
		return '/user/%s/' % self.computer_name