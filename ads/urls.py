from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    AdViewSet, ExchangeProposalViewSet,
    ad_list, ad_create, ad_detail, ad_delete,
    profile_view, propose_exchange, update_proposal_status,
    clear_sent_proposals, clear_received_proposals
)

router = DefaultRouter()
router.register(r'ads', AdViewSet)
router.register(r'exchange', ExchangeProposalViewSet)

urlpatterns = [
    path('ads/', ad_list, name='ad_list'),
    path('ads/create/', ad_create, name='ad_create'),
    path('ads/<int:pk>/', ad_detail, name='ad_detail'),
    path('ads/<int:pk>/delete/', ad_delete, name='ad_delete'),
    path('ads/<int:receiver_ad_id>/propose/', propose_exchange, name='propose_exchange'),
    path('profile/', profile_view, name='profile'),
    path('proposal/<int:proposal_id>/status/', update_proposal_status, name='update_proposal_status'),
    path('proposals/sent/clear/', clear_sent_proposals, name='clear_sent_proposals'),
    path('proposals/received/clear/', clear_received_proposals, name='clear_received_proposals'),
    path('api/', include(router.urls)),
]
