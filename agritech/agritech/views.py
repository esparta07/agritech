from django.shortcuts import render
from django.http.response import HttpResponse, Http404, HttpResponseNotFound, HttpResponseRedirect
from django.urls import reverse

# views

def index(request):
    return render(request, 'ecom/index-5.html')

def about(request):
    return render(request, 'ecom/about.html')

def faq(request):
    return render(request, 'ecom/faq.html')

def agro_sup(request):
    return render(request, 'ecom/blog.html')

def contact(request):
    return render(request, 'ecom/contact.html')

