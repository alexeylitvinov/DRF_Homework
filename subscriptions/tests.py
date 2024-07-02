from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from materials.models import Course
from users.models import User


class SubscriptionTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email='test_user@test.com', password='12345')
        self.course = Course.objects.create(user=self.user, title='test_course', description='test_description')
        self.client.force_authenticate(user=self.user)

    def test_subscription_create(self):
        url = reverse('subscriptions:manage_subscription')
        response = self.client.post(url, {'course_id': self.course.id, 'user_id': self.user.id})
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get('message'), 'Подписка добавлена')
        response = self.client.post(url, {'course_id': self.course.id, 'user_id': self.user.id})
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get('message'), 'Подписка удалена')
