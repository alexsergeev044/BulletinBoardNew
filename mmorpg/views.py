from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)

from .models import Ads, Response
from .forms import AdsForm
from .filters import AdsFilter, ResponseFilter


class AdsList(ListView):
    model = Ads
    ordering = '-date'
    template_name = 'AdsList.html'
    context_object_name = 'adsList'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = AdsFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class AdsDetail(DetailView):
    model = Ads
    template_name = 'AdsDetail.html'
    context_object_name = 'ads'


class AdsCreate(LoginRequiredMixin, CreateView):
    form_class = AdsForm
    model = Ads
    template_name = 'AdsEdit.html'
    context_object_name = 'ads'

    def form_valid(self, form):
        ads = form.save(commit=False)
        ads.author = self.request.user
        return super().form_valid(form)


class AdsEdit(LoginRequiredMixin, UpdateView):
    form_class = AdsForm
    model = Ads
    template_name = 'AdsEdit.html'
    context_object_name = 'ads'


class AdsDelete(LoginRequiredMixin, DeleteView):
    model = Ads
    template_name = 'AdsDelete.html'
    context_object_name = 'ads'
    success_url = reverse_lazy('ads_list')


class MyResponseList(LoginRequiredMixin, ListView):
    model = Response
    ordering = '-date'
    template_name = 'ResponseList.html'
    context_object_name = 'responseList'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset().filter(author=self.request.user)
        self.filterset = ResponseFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class AdsResponseList(LoginRequiredMixin, ListView):
    model = Response
    ordering = '-date'
    template_name = 'ResponseList.html'
    context_object_name = 'responseList'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset().filter(ad__author=self.request.user)
        self.filterset = ResponseFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class ResponseDetail(LoginRequiredMixin, DetailView):
    model = Response
    template_name = 'ResponseDetail.html'
    context_object_name = 'response'


class ResponseCreate(LoginRequiredMixin, CreateView):
    model = Response
    template_name = 'ResponseEdit.html'
    fields = ['text', ]
    context_object_name = 'response'

    def dispatch(self, request, *args, **kwargs):
        self.ad = get_object_or_404(Ads, pk=kwargs['pk'])
        return super(ResponseCreate, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        response = form.save(commit=False)
        if self.request.user == self.ad.author:
            form.add_error("", "Нельзя оставлять отклики на свои объявления!")
            return super().form_invalid(form)
        else:
            response.author = self.request.user
            response.ad = self.ad
            return super().form_valid(form)


class ResponseEdit(LoginRequiredMixin, UpdateView):
    model = Response
    template_name = 'ResponseEdit.html'
    fields = ['text', ]
    context_object_name = 'response'

    def form_valid(self, form):
        response = form.save(commit=False)
        if response.accepted:
            form.add_error("", "Нельзя редактировать принятый отклик!")
            return super().form_invalid(form)
        elif response.author != self.request.user:
            form.add_error("", "Нельзя редактировать чужой отклик!")
            return super().form_invalid(form)
        else:
            return super().form_valid(form)


class ResponseAccept(LoginRequiredMixin, UpdateView):
    model = Response
    template_name = 'ResponseEdit.html'
    fields = []
    context_object_name = 'response'

    def form_valid(self, form):
        response = form.save(commit=False)
        if response.accepted:
            form.add_error("", "Отклик уже был принят!")
            return super().form_invalid(form)
        elif response.ad.author != self.request.user:
            form.add_error("", "Нельзя принять отклик на чужое объявление!")
            return super().form_invalid(form)
        else:
            response.accepted = True
            return super().form_valid(form)


class ResponseDelete(LoginRequiredMixin, DeleteView):
    model = Response
    template_name = 'ResponseDelete.html'
    context_object_name = 'response'
    success_url = reverse_lazy('myresponse_list')
