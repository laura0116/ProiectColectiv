from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse_lazy

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
