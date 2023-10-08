from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver

from R4C.settings import EMAIL_HOST_USER
from orders.models import Order
from robots.models import Robot


