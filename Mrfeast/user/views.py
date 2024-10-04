from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm

class LoginUserView(View):
    def get(self, request):
        return render(request, 'authenticate/login.html', {})

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('inicio')
        else:
            messages.error(request, "There Was An Error Logging In, Try Again...")
            return redirect('login')

class LogoutUserView(View):
    def get(self, request):
        logout(request)
        return redirect('inicio')

class RegisterUserView(View):
    def get(self, request):
        form = UserCreationForm()
        return render(request, 'authenticate/register_user.html', {'form': form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('inicio')
        return render(request, 'authenticate/register_user.html', {'form': form})
