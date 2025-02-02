from django.urls import path 
from . import views 
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [ 
    path('', views.search_view), 
    path('search/', views.search_view, name='search_view'), 
    path('product/new/', views.product_create, name='product_create'), 
    path('product/<int:pk>/', views.product_detail, name='product_detail'), 
    path('product/<int:pk>/edit/',  views.product_update, name='product_update'), 
    path('product/<int:pk>/delete',  views.product_delete, name='product_delete'), 
    path('product/', views.product_list, name='product_list'),
    path('product/ranking', views.product_ranking,name='product_ranking')
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)