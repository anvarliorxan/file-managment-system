from django.db import models


class TimeStampedModel(models.Model):
	"""
	Abstract base class that provides self-updating 'created' and 'modified' fields.
	"""
	created = models.DateTimeField(auto_now_add=True)
	modified = models.DateTimeField(auto_now=True)

	class Meta:
		abstract = True

	@property
	def isedited(self):
		return False if self.created.strftime('%Y-%m-%d %H:%M:%S') == self.modified.strftime('%Y-%m-%d %H:%M:%S') else True
