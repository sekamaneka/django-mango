from django.http import HttpResponse
from django.shortcuts import render
from tkinter.constants import PAGES
from rango.forms import CategoryForm, PageForm
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

def add_page(request, category_name_slug):
    try:
        cat = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        cat = None
    if request.method == 'POST':
        form = PageForm(request.POST)
        
        if form.is_valid():
            if cat:
                page = form.save(commit=True)
                page.category = cat
                page.views = 0
                page.save()
                return category(request, category_name_slug)
        else:
            print(form.errors)
    
    else:
        form = PageForm()
    return render(request, 'rango/add_page.html', {'form' : form, 'category': cat})
    
def index(request):
    #return HttpResponse("Is this an Easter Egg?! <br/> <a href='/rango/about'>About</a>")
    ##context_dict = {'boldmessage': 'themessagegoeshere'}
    ##return render(request, 'rango/index.html', context_dict)
    category_list = Category.objects.order_by('-likes')[:10]
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
        context_dict['slug'] = category_name_slug
    except Category.DoesNotExist:
        pass
    return render(request, 'rango/category.html', context_dict)