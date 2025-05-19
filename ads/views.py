from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import HttpResponseForbidden

from rest_framework import viewsets, permissions
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.db.models import Q

from .models import Ad, ExchangeProposal
from .serializers import AdSerializer, ExchangeProposalSerializer
from .permissions import IsOwnerOrReadOnly, IsProposalParticipantOrReadOnly
from .forms import AdForm, ExchangeProposalForm


class AdViewSet(viewsets.ModelViewSet):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_queryset(self):
        queryset = Ad.objects.all()
        category = self.request.query_params.get('category')
        condition = self.request.query_params.get('condition')
        search = self.request.query_params.get('search')

        if category:
            queryset = queryset.filter(category__iexact=category)
        if condition:
            queryset = queryset.filter(condition__iexact=condition)
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | Q(description__icontains=search)
            )

        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ExchangeProposalViewSet(viewsets.ModelViewSet):
    queryset = ExchangeProposal.objects.all()
    serializer_class = ExchangeProposalSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsProposalParticipantOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(status='ожидает')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('ad_list')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


def home(request):
    if request.user.is_authenticated:
        return redirect('ad_list')

    form = AuthenticationForm(data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        login(request, form.get_user())
        return redirect('ad_list')

    return render(request, 'base.html', {'form': form, 'show_login_form': True})


def ad_list(request):
    ads = Ad.objects.all()

    search_query = request.GET.get("search", "")
    selected_category = request.GET.get("category", "")
    selected_condition = request.GET.get("condition", "")

    if search_query:
        ads = ads.filter(Q(title__icontains=search_query) | Q(description__icontains=search_query))
    if selected_category:
        ads = ads.filter(category__iexact=selected_category)
    if selected_condition:
        ads = ads.filter(condition__iexact=selected_condition)

    paginator = Paginator(ads, 16)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, 'ads/ad_list.html', {
        "ads": page_obj,
        "page_obj": page_obj,
        "search_query": search_query,
        "selected_category": selected_category,
        "selected_condition": selected_condition,
    })


def ad_detail(request, pk):
    ad = get_object_or_404(Ad, pk=pk)
    already_proposed = False

    if request.user.is_authenticated and ad.user != request.user:
        already_proposed = ExchangeProposal.objects.filter(
            ad_sender__user=request.user,
            ad_receiver=ad
        ).exists()

    return render(request, 'ads/ad_detail.html', {
        'ad': ad,
        'already_proposed': already_proposed
    })


@login_required
def ad_create(request):
    if request.method == 'POST':
        form = AdForm(request.POST)
        if form.is_valid():
            ad = form.save(commit=False)
            ad.user = request.user
            ad.save()
            return redirect('ad_detail', pk=ad.pk)
    else:
        form = AdForm()
    return render(request, 'ads/ad_form.html', {'form': form})


@login_required
def ad_delete(request, pk):
    ad = get_object_or_404(Ad, pk=pk)

    if ad.user != request.user:
        return HttpResponseForbidden("Вы не можете удалить это объявление.")

    if request.method == "POST":
        ad.delete()
        messages.success(request, "Объявление удалено.")
        return redirect('profile')

    return render(request, 'ads/ad_delete_confirm.html', {'ad': ad})


@login_required
def profile_view(request):
    user = request.user
    ads = Ad.objects.filter(user=user)

    paginator = Paginator(ads, 16)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    sent = ExchangeProposal.objects.filter(ad_sender__user=user)
    received = ExchangeProposal.objects.filter(ad_receiver__user=user)

    return render(request, 'ads/profile.html', {
        'my_ads': page_obj,
        'page_obj': page_obj,
        'sent_proposals': sent,
        'received_proposals': received,
    })


@login_required
def propose_exchange(request, receiver_ad_id):
    receiver_ad = get_object_or_404(Ad, pk=receiver_ad_id)

    if receiver_ad.user == request.user:
        messages.error(request, "Нельзя предложить обмен на своё объявление.")
        return redirect('ad_detail', pk=receiver_ad_id)

    my_ads = Ad.objects.filter(user=request.user)

    already_used_ids = ExchangeProposal.objects.filter(
        ad_sender__user=request.user
    ).values_list('ad_sender_id', flat=True)
    my_ads = my_ads.exclude(id__in=already_used_ids)

    if not my_ads.exists():
        messages.error(request, "Вы уже использовали все свои объявления для обмена.")
        return redirect('ad_detail', pk=receiver_ad_id)

    if request.method == 'POST':
        form = ExchangeProposalForm(request.POST)
        if form.is_valid():
            proposal = form.save(commit=False)
            proposal.ad_receiver = receiver_ad
            proposal.save()
            messages.success(request, "Предложение отправлено.")
            return redirect('ad_detail', pk=receiver_ad_id)
    else:
        form = ExchangeProposalForm()
        form.fields['ad_sender'].queryset = my_ads

    return render(request, 'ads/propose_exchange.html', {
        'form': form,
        'receiver_ad': receiver_ad
    })


@require_POST
@login_required
def update_proposal_status(request, proposal_id):
    proposal = get_object_or_404(ExchangeProposal, id=proposal_id)

    if proposal.ad_receiver.user != request.user:
        messages.error(request, "Вы не можете изменить это предложение.")
        return redirect('profile')

    new_status = request.POST.get('status')
    if new_status in ['принята', 'отклонена']:
        proposal.status = new_status
        proposal.save()
        messages.success(request, f"Предложение {new_status}.")
    else:
        messages.error(request, "Недопустимый статус.")

    return redirect('profile')


@require_POST
@login_required
def clear_sent_proposals(request):
    ExchangeProposal.objects.filter(ad_sender__user=request.user).delete()
    messages.success(request, "История отправленных предложений очищена.")
    return redirect('profile')


@require_POST
@login_required
def clear_received_proposals(request):
    ExchangeProposal.objects.filter(ad_receiver__user=request.user).delete()
    messages.success(request, "История входящих предложений очищена.")
    return redirect('profile')



