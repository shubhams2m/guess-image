from django.shortcuts import render
from .forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth import authenticate, logout, login
from django.views.generic import FormView, TemplateView
from artigone.models import *
from django.contrib.auth.models import Permission, User
from django.db.models import Q
from django.http import JsonResponse, HttpResponseRedirect,HttpResponse


class Register(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'register.html'

def logoutView(request):
    if request.user.is_authenticated:
        Game.objects.filter(Q(player1=request.user) | Q(player2=request.user)).update(status='inactive')
        logout(request)
        return HttpResponseRedirect('/login')
    return HttpResponseRedirect('/login')
