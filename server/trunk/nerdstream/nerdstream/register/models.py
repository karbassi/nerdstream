from google.appengine.ext import db

class Users(db.Model):
	first_name = db.StringProperty(required=True)
	last_name = db.StringProperty(required=True)
	computer_name = db.StringProperty()
	job_title = db.StringProperty(required=True)
	start_time = db.TimeProperty(required=True)
	end_time = db.TimeProperty(required=True)
	interval = db.IntegerProperty(default=5, required=True)
	last_update = db.DateTimeProperty(auto_now=1)
	creation_date = db.DateTimeProperty(auto_now_add=1)

	def __str__(self):
		return '%s' %self.question
	
	def get_absolute_url(self):
		return '/user/%s/' % self.key()