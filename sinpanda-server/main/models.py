from django.db import models


class TimeTable(models.Model):
    tt = models.IntegerField(default=0, blank=True, null=True)
    title = models.CharField(max_length=1000, blank=True, null=True)
    assignment = models.CharField(max_length=1000, blank=True, null=True)
    url = models.CharField(max_length=1000, blank=True, null=True)
    notiURL = models.CharField(max_length=1000, blank=True, null=True)
    resoURL = models.CharField(max_length=1000, blank=True, null=True)
    assiURL = models.CharField(max_length=1000, blank=True, null=True)
    zoomURL = models.CharField(max_length=1000, blank=True, null=True)


class Assignment(models.Model):
    ltitle = models.CharField(max_length=1000, blank=True, null=True)
    atitle = models.CharField(max_length=1000, blank=True, null=True)
    due = models.CharField(max_length=1000, blank=True, null=True)
    drop = models.CharField(max_length=1000, blank=True, null=True)
    assignment = models.CharField(max_length=1000, blank=True, null=True)
    url = models.CharField(max_length=1000, blank=True, null=True)


class Notification(models.Model):
    ann = models.CharField(max_length=1000, blank=True, null=True)
    url = models.CharField(max_length=1000, blank=True, null=True)
