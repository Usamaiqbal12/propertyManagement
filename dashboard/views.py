from django.http.response import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.
def settings(request):
    return HttpResponse('This is dashboard page')

@login_required
def dashboard(request):
    context = {'name': 'usama', 'age': 23, 'active_page': 'Dashboard'}
    return render(request, 'dashboard.html', context)

