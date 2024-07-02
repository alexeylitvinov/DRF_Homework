from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from materials.models import Course, Lesson
from users.models import User


class LessonTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email='test_user@test.com', password='12345')
        self.course = Course.objects.create(user=self.user, title='test_course', description='test_description')
        self.lesson = Lesson.objects.create(
            user=self.user,
            title='test_lesson',
            description='test_description',
            course=self.course
        )
        self.client.force_authenticate(user=self.user)

    def test_lesson_retrieve(self):
        url = reverse('materials:lesson_detail', kwargs={'pk': self.lesson.pk})
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get('title'), 'test_lesson')
        self.assertEqual(data.get('description'), 'test_description')

    def test_lesson_create(self):
        url = reverse('materials:lesson_create')
        data = {
            'user': self.user.pk,
            'title': 'test1_lesson1',
            'description': 'test1_description1',
            'course': self.course.pk
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.count(), 2)

    def test_lesson_update(self):
        url = reverse('materials:lesson_update', kwargs={'pk': self.lesson.pk})
        data = {
            'title': 'test2_lesson2',
            'description': 'test2_description2',
            'course': self.course.pk
        }
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get('title'), 'test2_lesson2')
        self.assertEqual(data.get('description'), 'test2_description2')

    def test_lesson_list(self):
        url = reverse('materials:lessons')
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data['results']), 1)

    def test_lesson_destroy(self):
        url = reverse('materials:lesson_delete', kwargs={'pk': self.lesson.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.count(), 0)
