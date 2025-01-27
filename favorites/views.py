from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Favorite
from search_app.models import Product
from django.shortcuts import render

@login_required
def profile_view(request):
    # 現在のログインユーザーのお気に入り楽曲を取得
    favorite_songs = Favorite.objects.filter(user=request.user).select_related('product')
    return render(request, 'profile.html', {'favorite_songs': favorite_songs})

@login_required
def add_to_favorites(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    Favorite.objects.get_or_create(user=request.user, product=product)
    return redirect('product_detail', pk=product_id)

@login_required
def remove_from_favorites(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    Favorite.objects.filter(user=request.user, product=product).delete()
    return redirect('product_detail', pk=product_id)