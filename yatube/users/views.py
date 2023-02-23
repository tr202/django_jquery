from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth import get_user_model
from rest_framework import permissions
from rest_framework.generics import CreateAPIView

from .serializers import UserSerialiser
from .forms import CreationForm

User = get_user_model()


class CreateUserView(CreateAPIView):
    model = User
    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerialiser


class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy('posts:index')
    template_name = 'users/signup.html'
