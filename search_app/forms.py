from django import forms 
from .models import Product
 
class SearchForm(forms.Form): 
    query = forms.CharField( 
        label='検索キーワード', 
        max_length=100, 
        required=False, 
        widget=forms.TextInput(attrs={'placeholder': '検索したいキーワードを入力'})    
    ) 
 
class ProductForm(forms.ModelForm): 
    class Meta: 
        model = Product 
        fields = ['name', 'description', 'price', 'category']
        labels = {
            'name': '名前',
            'description': '詳細',  
            'price' : '価格',
            'category' : 'カテゴリー'
        }