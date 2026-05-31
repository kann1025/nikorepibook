from django.db import models

class Recipe(models.Model):
    title = models.CharField(max_length=100)
    servings = models.IntegerField(default=2)
    reference_url = models.URLField(blank=True)
    memo = models.TextField(blank=True)

    def __str__(self):
        return self.title
