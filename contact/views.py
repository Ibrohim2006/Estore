from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ContactForm
from .models import AboutModel
from django.contrib.auth.decorators import login_required


@login_required(login_url='/accounts/login/')
def contact_view(request):
    about = AboutModel.objects.first()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('contact:contact')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ContactForm()
    d = {
        'form': form,
        'about': about,
    }

    return render(request, 'contact/contact.html', context=d)
