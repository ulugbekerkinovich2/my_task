from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from robots.models import Robot
import json


class RobotAPITest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_valid_robot_creation(self):
        data = {
            'serial': '12345',
            'model': 'A1',
            'version': '1.0',
        }
        response = self.client.post(reverse('robot_api'), json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Robot.objects.count(), 1)
