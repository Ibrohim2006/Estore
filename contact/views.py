from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ContactForm
from .models import AboutModel


def contact_view(request):
    about = AboutModel.objects.get(id=1)
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
