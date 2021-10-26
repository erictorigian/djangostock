from django.db import models

class Stock(models.Model):
    ticker = models.CharField(max_length=10)
    shares = models.IntegerField(default=0)

    def __str__(self):
        return self.ticker

class AppLog(models.Model):
    comment = models.TextField()
    version = models.CharField(max_length=5)
    updated = models.DateTimeField()

    def __str__(self):
        return self.comment

