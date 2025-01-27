from django.urls import path
from . import views

urlpatterns = [
    path('add/<int:product_id>/', views.add_to_favorites, name='add_to_favorites'),
    path('remove/<int:product_id>/', views.remove_from_favorites, name='remove_from_favorites'),
    path('profile/', views.profile_view, name='profile'),
]
