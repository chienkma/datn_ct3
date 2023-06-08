from django.db import models


class News(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.CharField(max_length=100)
    publish_date = models.DateField()
    image_url = models.URLField(
        blank=True,
        null=True,
        default="",
    )

    def __str__(self):
        return self.title


class Club(models.Model):
    name = models.CharField(max_length=100)
    logo_url = models.URLField()

    def __str__(self):
        return self.name
