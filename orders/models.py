from django.core.mail import send_mail
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from R4C import settings
from R4C.settings import EMAIL_HOST_USER
from customers.models import Customer
from robots.models import Robot


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    robot_serial = models.CharField(max_length=5, blank=False, null=False)
    robot_version = models.CharField(max_length=2, blank=False, null=False)
    robot_model = models.CharField(max_length=2, blank=False, null=False)

    def __str__(self):
        return f"{str(self.customer)}"


