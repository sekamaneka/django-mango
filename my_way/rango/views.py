from django.http import HttpResponse
from django.shortcuts import render
from django.models import Category

def index(request):
   # return HttpResponse("Is this an Easter Egg?! <br/> <a href='/rango/about'>About</a>")
    context_dict = {'boldmessage': 'themessagegoeshere'}
    return render(request, 'rango/index.html', context_dict)
def about(request):
    #return HttpResponse("what is this shit?<br/> <a href='/rango'>Back</a>")
    context_dict = {'italicmessage': 'themessagegoeshere'}
    return render(request, 'rango/about.html', context_dict)