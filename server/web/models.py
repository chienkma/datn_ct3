from django.db import models


class News(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.CharField(max_length=100)
    publish_date = models.DateField()
    image_url = models.URLField(
        blank=True,
        null=True,
        default="https://nhadepso.com/wp-content/uploads/2023/03/loa-mat-voi-nhung-hinh-anh-co-viet-nam-tuyet-dep-lam-hinh-nen_1.jpg",
    )

    def __str__(self):
        return self.title


class Club(models.Model):
    name = models.CharField(max_length=100)
    logo_url = models.URLField()

    def __str__(self):
        return self.name


class Match(models.Model):
    home_team = models.ForeignKey(
        Club, on_delete=models.CASCADE, related_name="home_matches"
    )
    away_team = models.ForeignKey(
        Club, on_delete=models.CASCADE, related_name="away_matches"
    )
    date = models.DateField()
    time = models.TimeField()
    home_score = models.IntegerField()
    away_score = models.IntegerField()

    def __str__(self):
        return f"{self.home_team.name} vs {self.away_team.name}"
