from django.db import models

# Create your models here.
class Title(models.Model):
    user_id = models.CharField(max_length=256)
    title = models.TextField()

    def __str__(self):
        return self.user_id

class Creator(models.Model):
    user_id = models.CharField(max_length=256)
    creator = models.CharField(max_length=256)

    def __str__(self):
        return self.user_id


class Response(models.Model):
    user_id = models.CharField(max_length=256)
    url = models.TextField()
 
    title0 = models.CharField(max_length=50, blank=True, null=True)
    detail0 = models.CharField(max_length=230, blank=True, null=True)
    callNumber0 = models.CharField(max_length=30, blank=True, null=True)

    title1 = models.CharField(max_length=50, blank=True, null=True)
    detail1 = models.CharField(max_length=230, blank=True, null=True)
    callNumber1 = models.CharField(max_length=30, blank=True, null=True)

    title2 = models.CharField(max_length=50, blank=True, null=True)
    detail2 = models.CharField(max_length=230, blank=True, null=True)
    callNumber2 = models.CharField(max_length=30, blank=True, null=True)

    title3 = models.CharField(max_length=50, blank=True, null=True)
    detail3 = models.CharField(max_length=230, blank=True, null=True)
    callNumber3 = models.CharField(max_length=30, blank=True, null=True)

    title4 = models.CharField(max_length=50, blank=True, null=True)
    detail4 = models.CharField(max_length=230, blank=True, null=True)
    callNumber4 = models.CharField(max_length=30, blank=True, null=True)

    title5 = models.CharField(max_length=50, blank=True, null=True)
    detail5 = models.CharField(max_length=230, blank=True, null=True)
    callNumber5 = models.CharField(max_length=30, blank=True, null=True)

    title6 = models.CharField(max_length=50, blank=True, null=True)
    detail6 = models.CharField(max_length=230, blank=True, null=True)
    callNumber6 = models.CharField(max_length=30, blank=True, null=True)

    title7 = models.CharField(max_length=50, blank=True, null=True)
    detail7 = models.CharField(max_length=230, blank=True, null=True)
    callNumber7 = models.CharField(max_length=30, blank=True, null=True)

    title8 = models.CharField(max_length=50, blank=True, null=True)
    detail8 = models.CharField(max_length=230, blank=True, null=True)
    callNumber8 = models.CharField(max_length=30, blank=True, null=True)

    title9 = models.CharField(max_length=50, blank=True, null=True)
    detail9 = models.CharField(max_length=230, blank=True, null=True)
    callNumber9 = models.CharField(max_length=30, blank=True, null=True)

    more = models.BooleanField(default=False)

    def __str__(self):
        return self.title0


