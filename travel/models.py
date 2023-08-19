from django.db import models

# Create your models here.
class Spot(models.Model):
    spot = models.CharField(max_length=100)