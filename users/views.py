from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import User
from .form import RegisterUserForm
from resume.models import Resume
from company.models import Company


#Registro de aplicantes
def register_applicant(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            var = form.save(commit=False)
            var.is_applicant = True
            var.username = var.email
            var.save()
            Resume.objects.create(user=var)
            messages.info(request, 'Sua conta foi criada com sucesso.')
            return redirect('login')
        else:
            messages.warning(request, 'Algo deu errado.')
            return redirect('register-applicant')
    else:
        form = RegisterUserForm()
        context = {'form':form}
        return render(request, 'users/register_applicant.html', context)
    


#Registro de empresa
def register_recruiter(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            var = form.save(commit=False)
            var.is_recruiter = True
            var.username = var.email
            var.save()
            Company.objects.create(user=var)
            messages.info(request, 'Sua conta foi criada com sucesso.')
            return redirect('login')
        else:
            messages.warning(request, 'Algo deu errado.')
            return redirect('register-recruiter')
    else:
        form = RegisterUserForm()
        context = {'form':form}
        return render(request, 'users/register_recruiter.html', context)
    


#Login de usuario
def login_user(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)
        if user is not None and user.is_active:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.warning(request, 'Algo deu errado.')
            return redirect('login')
    else:
        return render(request, 'users/login.html')
    

#Deslogar usuario
def logout_user(request):
    logout(request)
    messages.info(request, 'Sua sessão foi finalizada.')
    return redirect('login')