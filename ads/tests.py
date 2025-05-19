from django.test import TestCase
from django.contrib.auth.models import User
from .models import Ad, ExchangeProposal

class AdModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='pass')
        self.ad = Ad.objects.create(
            user=self.user,
            title='Тест Товар',
            description='Описание',
            category='Книги',
            condition='новое'
        )

    def test_ad_creation(self):
        self.assertEqual(self.ad.title, 'Тест Товар')
        self.assertEqual(self.ad.user.username, 'testuser')
        self.assertEqual(str(self.ad), 'Тест Товар')


class ExchangeProposalTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='sender', password='pass')
        self.user2 = User.objects.create_user(username='receiver', password='pass')

        self.ad_sender = Ad.objects.create(user=self.user1, title='Товар A', description='...', category='Одежда', condition='новое')
        self.ad_receiver = Ad.objects.create(user=self.user2, title='Товар B', description='...', category='Книги', condition='б/у')

        self.proposal = ExchangeProposal.objects.create(
            ad_sender=self.ad_sender,
            ad_receiver=self.ad_receiver,
            comment='Обменяй, пожалуйста',
            status='ожидает'
        )

    def test_exchange_proposal(self):
        self.assertEqual(self.proposal.status, 'ожидает')
        self.assertEqual(str(self.proposal), f'Обмен {self.ad_sender} → {self.ad_receiver} (ожидает)')
