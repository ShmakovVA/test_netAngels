from django.db import models


class Link(models.Model):
    """
    Model for storing links
    """
    url = models.URLField('Full link', max_length=1024)  # full url link
    hash = models.CharField(max_length=255)  # shorted url link
    click_count = models.IntegerField()  # count requests (redirections)
    datetime = models.DateTimeField(auto_now_add=True)  # creation datetime

    def inc_clicks(self):
        self.click_count += 1
        self.save()

    def __unicode__(self):
        return u'{} [{}]'.format(self.url, self.hash)

    def __str__(self):
        return '{} [{}]'.format(self.url, self.hash)
