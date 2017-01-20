import os

from django.contrib.auth.decorators import login_required
from django.forms import model_to_dict
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, render_to_response

# Create your views here.
from django.template import RequestContext
from django.urls import reverse
from django.urls import reverse_lazy

from LoginApp.models import Client
from TextMissing.forms import AddDocumentForm, UpdateDocumentForm
from TextMissing.models import Document
from text_missing import settings


@login_required(login_url=reverse_lazy('LoginApp:login'))
def documents_page(request):
    if request.user.is_staff:
        return redirect('admin:index')
    return render(request, "TextMissing/documents.html",
                  {'documents': Document.objects.all(), "has_permission": True})


@login_required(login_url=reverse_lazy('LoginApp:login'))
def delete_document(request, document_id):
    print(request.method)
    if request.method == "GET":
        files = Document.objects.filter(id=document_id)
        os.remove(os.path.join(settings.MEDIA_ROOT, files.first().file.name))
        files.delete()
    return redirect('TextMissing:documents')


@login_required(login_url=reverse_lazy('LoginApp:login'))
def add_document(request):
    current_user = Client.objects.filter(user=request.user).first()
    if request.method == 'POST':
        form = AddDocumentForm(current_user, request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('TextMissing:documents')
    else:
        form = AddDocumentForm(user=current_user)
    return render(request, 'TextMissing/upload_document.html', {
        'form': form
    })


def update_document(request, document_id):
    current_user = Client.objects.filter(user=request.user).first()
    current_document = Document.objects.filter(id=document_id).first()
    if request.method == 'POST':
        form = UpdateDocumentForm(current_user, document_id, request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('TextMissing:documents')
    else:
        form = UpdateDocumentForm(current_user, document_id, initial=model_to_dict(current_document))
    return render(request, 'TextMissing/upload_document.html', {
        'form': form
    })