from typing import Any
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import ListView,CreateView,UpdateView,DeleteView,FormView
from app.models import *
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

# Create your views here.

class CustomLoginView(LoginView):
    template_name = 'app/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('TaskList')

class RegisterPage(FormView):
    template_name = 'app/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('TaskList')

    def form_valid(self, form) -> HttpResponse:
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

class TaskList(LoginRequiredMixin ,ListView):
    model = Task
    context_object_name='tasks'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['count'] = context['tasks'].filter(complete=False).count()

        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks'] = context['tasks'].filter(
                title__icontains=search_input)
        context['search_input'] = search_input
        return context

class TaskCreate(CreateView):
    model = Task
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('TaskList')

    def form_valid(self, form) -> HttpResponse:
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)

class TaskUpdate(UpdateView):
    model = Task
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('TaskList')

class TaskDelete(DeleteView):
    model = Task
    success_url = reverse_lazy('TaskList')