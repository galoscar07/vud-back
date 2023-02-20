from django.db import models


class Footerlabels(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    label = models.CharField(max_length=100, blank=False)
    link = models.CharField(max_length=100, blank=False)

    class Meta:
        ordering = ['created']
