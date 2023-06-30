from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required(login_url='account_login')
def Home(request):
    return render(request,'paginas/home.html')

# Create your views here.
