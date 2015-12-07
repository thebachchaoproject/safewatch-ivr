from django.db import models

import jsonfield

from time import time

class Submit_report(models.Model):
    id = models.AutoField(primary_key=True)
    call_id = models.TextField(blank=True)
    called_to = models.TextField(blank=True)
    gender = models.TextField(blank=True)
    age = models.IntegerField(blank=True)
    incident_category = models.TextField(blank=True)
    reason_harassment = models.TextField(blank=True)
    date = models.TextField(blank=True)
    time = models.TextField(blank=True)
    location_lat = models.TextField(blank=True)
    location_long = models.TextField(blank=True)
    location = models.TextField(blank=True)
    police_q1 = models.TextField(blank=True)
    police_q2 = models.TextField(blank=True)
    police_q3 = models.TextField(blank=True)
    police_q4 = models.TextField(blank=True)
    police_q5 = models.TextField(blank=True)
    police_q6 = models.TextField(blank=True)
    police_q7 = models.TextField(blank=True)
    police_q8 = models.TextField(blank=True)
    police_q9 = models.TextField(blank=True)
    police_q10 = models.TextField(blank=True)
    police_q11 = models.TextField(blank=True)
    police_q12 = models.TextField(blank=True)
    infrastructure_r1 = models.IntegerField(blank=True)
    infrastructure_r2 = models.IntegerField(blank=True)
    transport_r1 = models.IntegerField(blank=True)
    transport_r2 = models.TextField(blank=True)
    transport_r3 = models.IntegerField(blank=True)
    transport_r4 = models.IntegerField(blank=True)
    transport_r5 = models.IntegerField(blank=True)
    transport_r6 = models.IntegerField(blank=True)
    

class Caller_details(models.Model):
    id = models.AutoField(primary_key=True)
    caller_number = models.TextField(blank=True)
    is_called = models.BooleanField(default=False)
