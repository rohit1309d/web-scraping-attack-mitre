from django.db import models
import re

# Create your models here.

class Link(models.Model):
    name = models.CharField(max_length = 20)
    link = models.CharField(max_length=200)
    detection = models.TextField(null=True)
    keywords = models.TextField(null=True)
    mitigate = models.TextField(null=True)

    def __str__(self):
        return self.name

    def get_words(self):
        res = re.findall(r'\w+', str(self.keywords))
        return res
    