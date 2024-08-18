from django.shortcuts import render, redirect
from .forms import UsuarioCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.
def registrar_usuario(request):
    if request.method == 'POST':
        form = UsuarioCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('admin:index')
    else:
        form = UsuarioCreationForm()
    return render(request, 'aplicativo/registrar_usuario.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('senha')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('chamados')
        else:
            messages.error(request, 'E-mail ou senha inválidos.')
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def chamados_view(request):
    return render(request, 'chamados.html')