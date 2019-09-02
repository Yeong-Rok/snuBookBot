from django.db import models

# Create your models here.
class Result(models.Model):
    user_id = models.CharField(max_length=256)
    req_title = models.TextField()
    res_title = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.search_result
