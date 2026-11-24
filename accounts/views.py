from django.contrib.auth import login
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.generic import FormView
from .forms import RegistrationForm


class RegisterView(FormView):
    template_name = "registration/register.html"
    form_class = RegistrationForm

    def get_success_url(self):
        target = self.request.POST.get("next") or self.request.GET.get("next")
        if target and url_has_allowed_host_and_scheme(target, allowed_hosts={self.request.get_host()}):
            return target
        return reverse("tasks:list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        return kwargs

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect(self.get_success_url())
