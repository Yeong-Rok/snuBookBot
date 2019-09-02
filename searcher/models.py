from django.db import models

# Create your models here.
class Result(models.Model):
    user_id = models.CharField(max_length=256)
    req_title = models.TextField()
    #res_title = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.req_title


class Response(models.Model):
    user_id = models.CharField(max_length=256)
    title = models.TextField()
    availability = models.CharField(max_length=256)
 
    title1 = models.TextField(blank=True, null=True)
    availability1 = models.CharField(max_length=256, blank=True, null=True)

    title2 = models.TextField(blank=True, null=True)
    availability2 = models.CharField(max_length=256, blank=True, null=True)

    def __str__(self):
        return self.title
