from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, render_to_response

# Create your views here.
from django.template import RequestContext
from django.urls import reverse
from django.urls import reverse_lazy

from TextMissing.forms import UploadDocumentForm
from TextMissing.models import Document


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
        Document.objects.filter(id=document_id).delete()
    return redirect('TextMissing:documents')

@login_required(login_url=reverse_lazy('LoginApp:login'))
def upload_document(request):
    if request.method == 'POST':
        form = UploadDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('TextMissing:documents')
    else:
        form = UploadDocumentForm()
    return render(request, 'TextMissing/upload_document.html', {
        'form': form
    })