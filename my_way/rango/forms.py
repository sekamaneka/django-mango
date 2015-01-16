from django import forms
from rango.models import Category, Page

class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=128, help_text="Please enter the name")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)
    def clean(self):
        cleaned_data = self.cleaned_data
        url = cleaned_data.get('url')
        if url and not url.startswith('http://'):
            url = 'http://' + url
            cleaned_data['url'] = url
            
            return cleaned_data
    class Meta:
        model = Category
        field = ('name',)
        
class PageForm(forms.ModelForm):
    title = forms.CharField(max_length=128, help_text="Please enter the title.")
    url = forms.URLField(max_length=200, help_text="Url Please")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    
    class Meta:
        model=Page
        exclude = ('category',)