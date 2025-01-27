from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
# サインアップビュー
def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('search_view')  # ログイン後のリダイレクト先
    else:
        form = UserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})
# ログインビュー
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('search_view')  # ログイン後のリダイレクト先
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})
# ログアウトビュー
def logout_view(request):
    logout(request)
    return redirect('search_view')  # ログアウト後のリダイレクト先