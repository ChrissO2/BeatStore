from django.shortcuts import render
from .forms import forms
from django.views import View
from django.core.mail import send_mail
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from .models import *
# Create your views here.

PRODUCER_EMAILS = ['kotrebadjango@gmail.com']


class ContactFormView(View):
    form_class = forms.NameForm
    template_name = 'shop/contact.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        ctx = {
            'form': form,
        }
        return render(request, self.template_name, ctx)

    def post(self, request, *args, **kwargs):
        form = forms.NameForm(request.POST)
        ctx = {
            'form': form,
            'msg': 'Something went wrong, try again.'
        }
        if form.is_valid():
            ctx['msg'] = 'Request send succesfully.'
            email = form.cleaned_data['email']
            content = form.cleaned_data['content']
            content += f"\n\nSender email: {email}"
            live_contact = form.cleaned_data['live_contact']
            if live_contact:
                content += f"\nLive contact: Yes"
            else:
                content += f"\nLive contact: No"
            user = None
            try:
                user = Customer.objects.get()
            except ObjectDoesNotExist:
                pass
            contact_request = ContactRequest(
                email=email,
                content=content,
                real_contact=live_contact,
            )
            if user:
                contact_request.user = user

            contact_request.save()

            send_mail(subject=f"Contact Request {contact_request.pk}",
                      message=content,
                      from_email=email,
                      recipient_list=PRODUCER_EMAILS)
            return render(request, self.template_name, ctx)
        return render(request, self.template_name, ctx)
