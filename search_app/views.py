from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Category 
from .forms import SearchForm,ProductForm
from django.core.paginator import Paginator 
 

def product_create(request): 
    if request.method == 'POST': 
        form = ProductForm(request.POST) 
        if form.is_valid(): 
            form.save() 
            return redirect('product_list') 
    else: 
        form = ProductForm() 
    return render(request, 'product_form.html', {'form': form}) 
 
def product_detail(request, pk): 
    product = get_object_or_404(Product, pk=pk) 
    return render(request, 'product_detail.html', {'product': product}) 
 
def product_update(request, pk): 
    product = get_object_or_404(Product, pk=pk) 
    if request.method == 'POST': 
        form = ProductForm(request.POST, instance=product) 
        if form.is_valid(): 
            form.save() 
            return redirect('product_detail', pk=product.pk) 
    else: 
        form = ProductForm(instance=product) 
   # product オブジェクトをテンプレートに渡す 
    return  render(request,  'product_form.html',  {'form':  form,  'product': product})

def product_delete(request, pk): 
    product = get_object_or_404(Product, pk=pk) 
    if request.method == 'POST': 
        product.delete() 
        return redirect('product_list') 
    return render(request, 'product_confirm_delete.html', {'product': product}) 
 
def product_list(request): 
    products = Product.objects.all() 
    return render(request, 'product_list.html', {'products': products})

def search_view(request): 
    form = SearchForm(request.GET or None) 
    results = Product.objects.all()  # クエリセットの初期化 

    if form.is_valid(): 
        query = form.cleaned_data['query'] 
        if query: 
            results = results.filter(name__icontains=query) 

    # カテゴリフィルタリング
    category_name = request.GET.get('category')
    if category_name:
        # カテゴリ名が一致するものを取得（部分一致ではなく、完全一致に変更）
        category = Category.objects.filter(name=category_name).first()
        if category:
            # 商品をカテゴリでフィルタリング（ForeignKeyのためcategory_idを使用）
            results = results.filter(category_id=category.id)
        else:
            results = results.none()  # 存在しないカテゴリの場合、結果を空にする

    # 価格のフィルタリング
    min_price = request.GET.get('min_price') 
    max_price = request.GET.get('max_price')
    if min_price: 
        results = results.filter(price__gte=min_price) 
    if max_price: 
        results = results.filter(price__lte=max_price) 
     
    # 並び替え処理 
    sort_by = request.GET.get('sort', 'name') 
    if sort_by == 'price_asc': 
        results = results.order_by('price') 
    elif sort_by == 'price_desc': 
        results = results.order_by('-price') 
 
    # ページネーション処理 
    paginator = Paginator(results, 10) 
    page_number = request.GET.get('page') 
    page_obj = paginator.get_page(page_number)

    # カテゴリリストをテンプレートに渡す
    categories = Cat