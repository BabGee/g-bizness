from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    url = models.URLField(max_length=150)

    def __str__(self):
        return f'{self.name} {self.url}'