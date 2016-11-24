from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.
from django.forms import ValidationError

from LoginApp.forms import LoginForm, CustomizeAccountForm


@login_required(login_url=reverse_lazy('LoginApp:login'))
def main_page(request):
    if request.user.is_staff:
        return redirect('admin:index')
    if request.user.groups.filter(name="contributor").count():
        return render(request, "LoginApp/main_page.html", {'role': 'contributor'})

def login_page(request):
    new_form = LoginForm()
    if request.method != 'POST':
        return render(request, "LoginApp/login.html", {'form': new_form})
    auth_form = LoginForm(data=request.POST)
    if auth_form.is_valid():
        username = auth_form.cleaned_data["username"]
        password = auth_form.cleaned_data["password"]
        user = authenticate(username=username, password=password)
        if not user:
            auth_form.add_error(None, ValidationError("User or password wrong!"))
            return render(request, "LoginApp/login.html", {'form': auth_form})

        login(request, user)
        if "next" not in request.GET:
            return redirect("LoginApp:main")
        else:
            return HttpResponseRedirect(request.GET["next"])
    else:
        return render(request, "LoginApp/login.html", {'form': auth_form})


@login_required(login_url=reverse_lazy('LoginApp:login'))
def logout_page(request):
    logout(request)
    return render(request, "LoginApp/logout.html", {"title": "Logged out!"})


@login_required(login_url=reverse_lazy('LoginApp:login'))
def change_account(request):
    if request.method != 'POST':
        newForm = CustomizeAccountForm(user=request.user)
        newForm.fields["username"].initial = request.user.username;
        return render(request, "LoginApp/change_account.html", {'form': newForm})

    form = CustomizeAccountForm(user=request.user, data=request.POST)
    if form.is_valid():
        form.save()
        update_session_auth_hash(request, form.user)
        if not form.user.client_set.first().is_activated:
            obj = form.user.client_set.first()
            obj.is_activated = True
            obj.save()
        return render(request, "LoginApp/done_change_account.html", {'title': "Account updated!"})
    else:
        return render(request, "LoginApp/change_account.html", {'form': form})
