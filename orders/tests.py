import json
from django.test import TestCase
from django.urls import reverse
from customers.models import Customer
from robots.models import Robot
from orders.models import Order

class OrderViewTest(TestCase):

    def test_valid_order_creation(self):
        data = {
            'serial': '12345',
            'model': 'A1',
            'version': '1.0',
            'email': 'test@example.com'
        }
        response = self.client.post(reverse('order_api'), json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Мы уведомим вас по электронной почте, когда появится данный тип робота'})
        self.assertEqual(Customer.objects.count(), 1)
        self.assertEqual(Order.objects.count(), 1)

    def test_invalid_order_creation_missing_fields(self):
        data = {
            'serial': '12345',
            'model': 'A1'
        }
        response = self.client.post(reverse('order_api'), json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'error': 'Отсутствуют обязательные поля в запросе'})
        self.assertEqual(Customer.objects.count(), 0)
        self.assertEqual(Order.objects.count(), 0)

    def test_invalid_order_creation_invalid_json(self):
        invalid_json_data = 'Invalid JSON data'
        response = self.client.post(reverse('order_api'), invalid_json_data, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'error': 'Неверные данные JSON'})
        self.assertEqual(Customer.objects.count(), 0)
        self.assertEqual(Order.objects.count(), 0)

    def test_invalid_http_method(self):
        response = self.client.get(reverse('order_api'))
        self.assertEqual(response.status_code, 405)
        self.assertEqual(response.json(), {'error': 'Недопустимый метод запроса'})
        self.assertEqual(Customer.objects.count(), 0)
        self.assertEqual(Order.objects.count(), 0)

    def test_order_creation_robot_not_exists(self):
        data = {
            'serial': '12345',
            'model': 'A1',
            'version': '1.0',
            'email': 'test@example.com'
        }
        response = self.client.post(reverse('order_api'), json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Мы уведомим вас по электронной почте, когда появится данный тип робота'})
        self.assertEqual(Customer.objects.count(), 1)
        self.assertEqual(Order.objects.count(), 1)

    def test_order_creation_customer_exists(self):
        customer = Customer.objects.create(email='test@example.com')
        data = {
            'serial': '12345',
            'model': 'A1',
            'version': '1.0',
            'email': 'test@example.com'
        }
        response = self.client.post(reverse('order_api'), json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
                         {'message': 'Мы уведомим вас по электронной почте, когда появится данный тип робота'})
        self.assertEqual(Customer.objects.count(), 1)
        self.assertEqual(Order.objects.count(), 1)
