import os

from django.contrib.auth.decorators import login_required, user_passes_test
from django.forms import model_to_dict
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, render_to_response

# Create your views here.
from django.template import RequestContext
from django.urls import reverse
from django.urls import reverse_lazy

from LoginApp.models import Client
from TextMissing.forms import AddDocumentForm, RectorDispositionForm, NecessityRequestForm, UpdateRectorDisposition, \
    UpdateNecessityRequest
from TextMissing.forms import AddDocumentForm, UpdateDocumentForm
from TextMissing.models import Document, DocumentType, RectorDispositionDocument, UploadedDocument, \
    NecessityRequestDocument
from TextMissing.utils.check_user import is_manager, is_contributor, is_manager_or_contributor
from TextMissing.utils.document_manager import DocumentManager
from text_missing import settings


@login_required(login_url=reverse_lazy('LoginApp:login'))
def documents_page(request):
    if request.user.is_staff:
        return redirect('admin:index')
    return render(request, "TextMissing/documents.html",
                  {'documents': Document.objects.all(), "document_types": DocumentType, "has_permission": True,
                   "is_manager_or_contributor": is_manager_or_contributor(request.user) })


@login_required(login_url=reverse_lazy('LoginApp:login'))
@user_passes_test(is_manager_or_contributor,login_url=reverse_lazy('LoginApp:login'))
def delete_document(request, document_id):
    print(request.method)
    if request.method == "GET":
        # files = Document.objects.filter(id=document_id)
        # os.remove(os.path.join(settings.MEDIA_ROOT, files.first().file.name))
        # files.delete()
        DocumentManager.remove_document(document_id)
    return redirect('TextMissing:documents')


@login_required(login_url=reverse_lazy('LoginApp:login'))
@user_passes_test(is_manager_or_contributor,login_url=reverse_lazy('LoginApp:login'))
def add_document(request, document_type):
    options = {
        DocumentType.UPLOADED: AddDocumentForm,
        DocumentType.DR: RectorDispositionForm,
        DocumentType.RN: NecessityRequestForm
    }
    return upload_form(request, options[document_type])


def update_form(request, document_id, update_form_class, document_class):
    current_user = Client.objects.filter(user=request.user).first()
    current_document = document_class.objects.filter(id=document_id).first()
    if request.method == 'POST':
        form = update_form_class(current_user, document_id, request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('TextMissing:documents')
    else:
        form = update_form_class(current_user, document_id, initial=model_to_dict(current_document))
    return render(request, 'TextMissing/upload_document.html', {
        'form': form
    })


@user_passes_test(is_manager_or_contributor, login_url=reverse_lazy('LoginApp:login'))
def update_document(request, document_id):
    options = {
        DocumentType.UPLOADED: UpdateDocumentForm,
        DocumentType.DR: UpdateRectorDisposition,
        DocumentType.RN: UpdateNecessityRequest
    }
    options_doc_type = {
        DocumentType.UPLOADED: UploadedDocument,
        DocumentType.DR: RectorDispositionDocument,
        DocumentType.RN: NecessityRequestDocument
    }
    document_type = Document.objects.filter(id=document_id).first().type
    return update_form(request,document_id, options[document_type],options_doc_type[document_type])


@login_required(login_url=reverse_lazy('LoginApp:login'))
def upload_form(request, document_form_class):
    current_user = Client.objects.filter(user=request.user).first()
    if request.method == 'POST':
        form = document_form_class(current_user, request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('TextMissing:documents')
    else:
        form = document_form_class(user=current_user)
    return render(request, 'TextMissing/upload_document.html', {
        'form': form
    })


@login_required(login_url=reverse_lazy('LoginApp:login'))
def zones(request):
    return render(request, 'TextMissing/zones.html')


@login_required(login_url=reverse_lazy('LoginApp:login'))
def work_zone(request):
    files = Document.objects.all()
    current_user = Client.objects.filter(user=request.user).first()
    documents =[]
    if request.method == 'GET':
        for file in files:
            if file.status == 'draft':
                if current_user.type == 'manager':
                    documents.append(file)
                elif file.author == current_user:
                    documents.append(file)
        return render(request, "TextMissing/work_zone.html",
                  {'documents': documents, "has_permission": True})


@login_required(login_url=reverse_lazy('LoginApp:login'))
def initiate_zone(request):
    files = Document.objects.all()
    current_user = Client.objects.filter(user=request.user).first()
    documents =[]
    if request.method == 'GET':
        for file in files:
            if file.status == 'final' or file.status == 'finalRevised':
               if file.author == current_user:
                    documents.append(file)
        return render(request, "TextMissing/initiate_zone.html",
                  {'documents': documents, "has_permission": True})


@login_required(login_url=reverse_lazy('LoginApp:login'))
def task_zone(request):
    files = Document.objects.all()
    current_user = Client.objects.filter(user=request.user).first()
    documents =[]
    if request.method == 'GET':
        for file in files:
            if file.status == 'final' or file.status == 'finalRevised':
               if file.author != current_user:
                    documents.append(file)
        return render(request, "TextMissing/task_zone.html",
                  {'documents': documents, "has_permission": True})


@login_required(login_url=reverse_lazy('LoginApp:login'))
def finished_zone(request):
    files = Document.objects.all()
    documents =[]
    if request.method == 'GET':
        for file in files:
            if file.status == 'blocked':
                documents.append(file)
        return render(request, "TextMissing/task_zone.html",
                  {'documents': documents, "has_permission": True})
