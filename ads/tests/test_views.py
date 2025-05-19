from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from ads.models import Ad, ExchangeProposal

class ViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(username='user1', password='pass')
        self.user2 = User.objects.create_user(username='user2', password='pass')

        self.ad1 = Ad.objects.create(
            user=self.user1,
            title='Тест 1',
            description='Описание 1',
            image_url='https://example.com/img1.jpg',
            category='Книги',
            condition='новое'
        )
        self.ad2 = Ad.objects.create(
            user=self.user2,
            title='Тест 2',
            description='Описание 2',
            image_url='https://example.com/img2.jpg',
            category='Одежда',
            condition='б/у'
        )

    def test_ad_list_view(self):
        response = self.client.get(reverse('ad_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.ad1.title)

    def test_ad_detail_view(self):
        response = self.client.get(reverse('ad_detail', args=[self.ad1.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.ad1.title)

    def test_login_required_for_ad_create(self):
        response = self.client.get(reverse('ad_create'))
        self.assertEqual(response.status_code, 302)

    def test_create_ad_authenticated(self):
        self.client.login(username='user1', password='pass')
        response = self.client.post(reverse('ad_create'), {
            'title': 'Новый тест',
            'description': 'Описание',
            'image_url': 'https://example.com/test.jpg',
            'category': 'Книги',
            'condition': 'новое'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Ad.objects.filter(title='Новый тест').exists())

    def test_delete_own_ad(self):
        self.client.login(username='user1', password='pass')
        response = self.client.post(reverse('ad_delete', args=[self.ad1.id]))
        self.assertRedirects(response, reverse('profile'))
        self.assertFalse(Ad.objects.filter(id=self.ad1.id).exists())

    def test_delete_foreign_ad_forbidden(self):
        self.client.login(username='user1', password='pass')
        response = self.client.post(reverse('ad_delete', args=[self.ad2.id]))
        self.assertEqual(response.status_code, 403)

    def test_pagination(self):
        self.client.login(username='user1', password='pass')
        for i in range(70):
            Ad.objects.create(
                user=self.user1,
                title=f'Объявление {i}',
                description='Описание',
                category='Книги',
                condition='новое'
            )
        response = self.client.get(reverse('ad_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Объявление 0')
