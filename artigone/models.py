from django.db import models
from django.conf import settings


class Game(models.Model):
    player1 = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='player1', on_delete=models.PROTECT, null=True)
    player2 = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='player2', on_delete=models.PROTECT, null=True)
    score = models.IntegerField()
    status = models.CharField(max_length=50)
    first_solution = models.CharField(max_length=100,null=True)
    second_solution = models.CharField(max_length=100,null=True)

class PrimaryImage(models.Model):
    primary_image_url = models.URLField(max_length=500)
    def __str__(self):
        return self.primary_image_url

class SecondaryImage(models.Model):
    secondary_image_url = models.URLField(max_length=500)

class Question(models.Model):
    game = models.ForeignKey(Game, null=False, on_delete=models.PROTECT)
    image = models.ForeignKey(PrimaryImage, null=True, on_delete=models.PROTECT)

class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.PROTECT)
    image = models.ForeignKey(SecondaryImage, null=True, on_delete=models.PROTECT)
