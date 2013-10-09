from django.db import models

import datetime
from django.utils import timezone

class Upload(models.Model):
    
    def __unicode__(self):
        return self.filename
    
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
    
    filename = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')