import json

from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from customers.models import Customer
from orders.models import Order
from robots.models import Robot


@csrf_exempt
def order(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            serial = data.get('serial')
            model = data.get('model')
            version = data.get('version')
            email = data.get('email')
            if serial and model and version and email:
                if Robot.objects.filter(model=model, serial=serial, version=version).exists():
                    customer, created = Customer.objects.get_or_create(email=email)

                    instance_order = Order.objects.create(customer=customer,
                                                          robot_serial=serial,
                                                          robot_version=version,
                                                          robot_model=model)
                    instance_order.save()

                    return JsonResponse({'message': 'Ваш заказ принят'})
                else:
                    customer, created = Customer.objects.get_or_create(email=email)
                    instance_new_order = Order.objects.create(robot_serial=serial,
                                                              robot_version=version,
                                                              robot_model=model,
                                                              customer=customer)
                    instance_new_order.save()
                    return JsonResponse(
                        {'message': 'Мы уведомим вас по электронной почте, когда появится данный тип робота'})
            else:
                return JsonResponse({'error': 'Отсутствуют обязательные поля в запросе'}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Неверные данные JSON"}, status=400)
    else:
        return JsonResponse({"error": "Недопустимый метод запроса"}, status=405)


