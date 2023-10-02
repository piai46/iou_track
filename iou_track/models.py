from django.db import models

class User(models.Model):
    name = models.CharField(max_length=256, unique=True, blank=False, null=False)
    owes = models.JSONField(blank=True, null=True, default=dict)
    owe_by = models.JSONField(blank=True, null=True, default=dict)
    balance = models.FloatField(default=0)