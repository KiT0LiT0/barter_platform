from django.test import TestCase
from ads.forms import AdForm, ExchangeProposalForm
from ads.models import Ad
from django.contrib.auth.models import User

class FormTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='pass')
        self.user2 = User.objects.create_user(username='user2', password='pass')
        self.ad1 = Ad.objects.create(
            user=self.user1,
            title='Тест 1',
            description='Описание 1',
            image_url='https://example.com/image.jpg',
            category='Книги',
            condition='новое'
        )
        self.ad2 = Ad.objects.create(
            user=self.user2,
            title='Тест 2',
            description='Описание 2',
            image_url='https://example.com/image2.jpg',
            category='Электроника',
            condition='б/у'
        )

    def test_ad_form_valid(self):
        form_data = {
            'title': 'Пример',
            'description': 'Описание',
            'image_url': 'https://example.com/pic.jpg',
            'category': 'Одежда',
            'condition': 'б/у'
        }
        form = AdForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_ad_form_missing_required_field(self):
        form_data = {
            'description': 'Описание без названия',
            'image_url': 'https://example.com/pic.jpg',
            'category': 'Книги',
            'condition': 'новое'
        }
        form = AdForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)

    def test_exchange_proposal_form_valid(self):
        form_data = {
            'ad_sender': self.ad1.id,
            'comment': 'Хочу обменять'
        }
        form = ExchangeProposalForm(data=form_data)
        form.fields['ad_sender'].queryset = Ad.objects.all()
        self.assertTrue(form.is_valid())

    def test_exchange_proposal_form_missing_sender(self):
        form_data = {
            'comment': 'Нет отправителя'
        }
        form = ExchangeProposalForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('ad_sender', form.errors)
