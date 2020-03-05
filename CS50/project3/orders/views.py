from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required


# Create your views here.
def index(request):
    return HttpResponse("Project 3: TODO")

@login_required
def my_view(request):
    return HttpResponse("Fuck yeah")
