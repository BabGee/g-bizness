from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    #rating = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.name} {self.description}'