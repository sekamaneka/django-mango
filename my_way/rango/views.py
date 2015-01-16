from django.http import HttpResponse
from django.shortcuts import render
from tkinter.constants import PAGES
from rango.forms import CategoryForm
from rango.models import Category, Page

def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        
        if form.is_valid():
            form.save(commit=True)
            return index(request)
        else:
            print(form.errors)
    else:
        form = CategoryForm()
    return render(request, 'rango/add_category.html', {'form' : form})
    
def index(request):
    #return HttpResponse("Is this an Easter Egg?! <br/> <a href='/rango/about'>About</a>")
    ##context_dict = {'boldmessage': 'themessagegoeshere'}
    ##return render(request, 'rango/index.html', context_dict)
    category_list = Category.objects.order_by('-likes')[:5]
    context_dict = {'categories' : category_list}
    return render(request, 'rango/index.html', context_dict)
def about(request):
    #return HttpResponse("what is this shit?<br/> <a href='/rango'>Back</a>")
    context_dict = {'italicmessage': 'themessagegoeshere'}
    return render(request, 'rango/about.html', context_dict)
def category(request, category_name_slug):
    context_dict = {}
    try:
        category = Category.objects.get(slug=category_name_slug)
        context_dict['category_name'] = category.name
        pages = Page.objects.filter(category=category)
        context_dict['pages'] = pages
        context_dict['category'] = Category
    except Category.DoesNotExist:
        pass
    return render(request, 'rango/category.html', context_dict)