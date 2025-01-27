from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Category 
from .forms import SearchForm,ProductForm
from django.core.paginator import Paginator 
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank 
from django.contrib.auth.decorators import login_required
from favorites.models import Favorite
from django.conf import settings
from django.db.models import Q
from django.contrib import messages

@login_required
def product_create(request): 
    if request.method == 'POST': 
        form = ProductForm(request.POST,request.FILES) 
        if form.is_valid(): 
            form.save() 
            return redirect('product_list') 
    else: 
        form = ProductForm() 
    return render(request, 'product_form.html', {'form': form})



def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.view_count += 1
    product.save()

    is_favorited = False
    if request.user.is_authenticated:
        is_favorited = Favorite.objects.filter(user=request.user, product=product).exists()
    
    related_products = Product.objects.filter(category=product.category).exclude(pk=pk)[:3]

    return render(request, 'product_detail.html', {
        'product': product,
        'is_favorited': is_favorited,
        'related_products': related_products,
    })
@login_required 
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
@login_required
def product_delete(request, pk): 
    product = get_object_or_404(Product, pk=pk)
    
    if request.method == 'POST': 
        entered_password = request.POST.get('admin_password')
        if entered_password == settings.ADMIN_DELETE_PASSWORD:
            product.delete()
            messages.success(request, f'商品 "{product.title}" を削除しました。')
            return redirect('product_list')
        else:
            messages.error(request, '認証に失敗しました。正しいパスワードを入力してください。')

    return render(request, 'product_confirm_delete.html', {'product': product})
def product_list(request): 
    products = Product.objects.all() 
    return render(request, 'product_list.html', {'products': products})

def search_view(request):
    form = SearchForm(request.GET or None)
    results = Product.objects.all()

    if form.is_valid():
        query = form.cleaned_data['query']
        if query:
            # タイトルまたはアーティスト名で部分一致検索
            results = results.filter(
                Q(title__icontains=query) | Q(artist__icontains=query)
            )

    category_name = request.GET.get('category')
    if category_name:
        category = Category.objects.filter(name=category_name).first()
        if category:
            results = results.filter(category_id=category.id)
        else:
            results = results.none()

    sort_option = request.GET.get('sort', 'title')  # デフォルトを 'title' に設定
    if sort_option == 'release_date':
        results = results.order_by('release_date')
    elif sort_option == 'release_date_desc':
        results = results.order_by('-release_date')
    else:
        results = results.order_by('title')

    paginator = Paginator(results, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    categories = Category.objects.all()

    return render(request, 'search.html', {
        'form': form,
        'page_obj': page_obj,
        'results': results,
        'categories': categories,
        'selected_category': category_name,
        'sort_option': sort_option,
    })

def product_ranking(request):
    products = Product.objects.order_by('-view_count')[:10]  # 閲覧数の多い順にトップ10を取得
    return render(request, 'product_ranking.html', {'products': products})