from django.conf import settings
from django.db import models

class Category(models.Model):
    ''' Holder model for categories from tender.
        This model should be populated using sync_categories in tenderize.helpers.
    '''

    name = models.CharField(max_length=100)
    permalink = models.CharField(max_length=100)
    url = models.URLField()
    
    def create_discussion(self, title, body, user, public=True):
        from tenderize.helpers import tender_api
        
        return tender_api().create_discussion(title, body, self.id, user.email, user.username, public)
