from django.db import models
from django.contrib.auth.models import User

class Ad(models.Model):
    CATEGORY_CHOICES = [
        ('Книги', 'Книги'),
        ('Электроника', 'Электроника'),
        ('Одежда', 'Одежда'),
    ]

    CONDITION_CHOICES = [
        ('новое', 'Новое'),
        ('б/у', 'Б/у'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    image_url = models.URLField(blank=True, null=True)
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES)
    condition = models.CharField(max_length=50, choices=CONDITION_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class ExchangeProposal(models.Model):
    STATUS_CHOICES = [
        ('ожидает', 'Ожидает'),
        ('принята', 'Принята'),
        ('отклонена', 'Отклонена'),
    ]

    ad_sender = models.ForeignKey(
        Ad, on_delete=models.CASCADE, related_name='sent_proposals'
    )
    ad_receiver = models.ForeignKey(
        Ad, on_delete=models.CASCADE, related_name='received_proposals'
    )
    comment = models.TextField(blank=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='ожидает'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Обмен {self.ad_sender} → {self.ad_receiver} ({self.status})"
