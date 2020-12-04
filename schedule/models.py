import datetime

from django.db import models


# Create your models here.

class Appointment(models.Model):
    create_at = models.DateTimeField(verbose_name="created at", auto_now=True)
    date = models.DateField(verbose_name="appointment date", blank=True, null=True)
    time = models.TimeField(verbose_name="appointment time", blank=True, null=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.EmailField(max_length=100, blank=True)
    phone = models.CharField(max_length=14, blank=False)
    birthday = models.DateField(verbose_name="birthday")
    description = models.TextField(verbose_name="description")

    class Meta:
        verbose_name = "Appointment"
        verbose_name_plural = verbose_name + "s"
        ordering = ["-date", "time"]

    def __str__(self):
        return str(self.date) + " " + str(self.time) + ", " + self.first_name + self.last_name


# class WaitList(models.Model):
#     joined = models.DateTimeField(verbose_name="created at", auto_now=True)
#     first_name = models.CharField(max_length=20)
#     last_name = models.CharField(max_length=20)
#     email = models.EmailField(max_length=100, blank=True)
#     phone = models.CharField(max_length=14)
#     birthday = models.DateField(verbose_name="birthday")
#     picked = models.BooleanField(default=False)
#
#     class Meta:
#         verbose_name = "wait list"
#         ordering = ["joined", "picked"]
#
#     def __str__(self):
#         return self.first_name + " " + self.last_name
