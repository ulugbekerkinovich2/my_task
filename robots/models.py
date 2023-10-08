from django.core.mail import send_mail
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.http import HttpResponse

from R4C import settings



class Robot(models.Model):
    serial = models.CharField(max_length=5, blank=False, null=False)
    model = models.CharField(max_length=2, blank=False, null=False)
    version = models.CharField(max_length=2, blank=False, null=False)
    created = models.DateTimeField(blank=False, null=False)

    def __str__(self):
        return f'model: {self.model} version: {self.version} serial: {self.serial}'

@receiver(post_save, sender=Robot)
def notify_on_robot_arrival(sender, instance, **kwargs):
    from orders.models import Order
    robot_serial = instance.serial
    robot_version = instance.version
    robot_model = instance.model

    if robot_serial and robot_version and robot_model:
        try:
            order = Order.objects.filter(
                robot_serial=robot_serial,
                robot_model=robot_version,
                robot_version=robot_model
            ).first()

            if order:
                email = order.customer.email
                subject = 'Новый робот в наличии'
                message = (
                    f'Недавно вы интересовались нашим роботом модели'
                    f' {robot_version} и '
                    f'серии {robot_serial}. '
                    f'Хотим сообщить, что этот робот теперь в наличии. '
                    f'Если он вас заинтересовал, пожалуйста, свяжитесь с нами для заказа.')
                recipient_list = [email]

                try:
                    send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list, fail_silently=False)
                except Exception as e:
                    return HttpResponse(f'Ошибка отправки письма: {str(e)}')
            else:
                return HttpResponse('Робот не найден в наличии ')
        except Robot.DoesNotExist:
            return HttpResponse('Робот не найден в наличии ')
