from django.http import HttpResponse
from django.shortcuts import render
from tkinter.constants import PAGES
from rango.forms import CategoryForm, PageForm
from rango.models import Category, Page
from datetime import datetime

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
                page = form.save(commit=False)
                page.category = cat
                page.views = 0
                page.save()
                return category(request, category_name_slug)
        else:
            print(form.errors)
    
    else:
        form = PageForm()
    return render(request, 'rango/add_page.html', {'form' : form, 'category': cat, 'slug': category_name_slug})
    
def index(request):
    category_list = Category.objects.all()
    page_list = Page.objects.all()
    context_dict = {'categories' : category_list, 'pages': page_list}
    
    visits = request.session.get('visits')
    if not visits:
        visits = 1
    reset_last_visit_time = False
    
    last_visit = request.session.get('last_visit')
    if last_visit:
        last_visit_time = datetime.strptime(last_visit[:-7], '%Y-%m-%d %H:%M:%S')
        
        if (datetime.now() - last_visit_time).seconds > 10:
            visits += 1
            reset_last_visit_time = True
    else:
        reset_last_visit_time = True
        
    if reset_last_visit_time:
        request.session['last_visit'] = str(datetime.now())
        request.session['visits'] = visits
    context_dict['visits'] = visits
    
    response = render(request, 'rango/index.html', context_dict)
    return response

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