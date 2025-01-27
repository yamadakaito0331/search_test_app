from django.urls import path
from . import views  # 作成したviews.pyをインポート

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),  # 登録ページのURL
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]