import datetime

from django import template
from django.db.models import Count

from ..models import Appointment

register = template.Library()


@register.simple_tag
def get_waitlist_count(date):
    date = datetime.datetime.strptime(date, "%m/%d/%Y").date().strftime("%Y-%m-%d")
    return Appointment.objects.filter(date=date, time=None).count()


@register.simple_tag
def get_appointment_count(date):
    date = datetime.datetime.strptime(date, "%m/%d/%Y").date().strftime("%Y-%m-%d")
    return Appointment.objects.filter(date=date).exclude(time=None).count()