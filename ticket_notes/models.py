from django.db import models

class BookmarkedEvent(models.Model):
    event_name = models.CharField(max_length=200)
    local_date = models.DateField()
    local_time = models.TimeField()
    venue = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    image_url = models.URLField(max_length=1024, blank=True, null=True) 
    note = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.event_name
