from django.urls import path
from app_cadastro import views
from django.contrib import admin
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('auth/register/', views.register, name='register'),
    path('auth/login/', views.login, name='login'),
    path('auth/logout/', views.logout, name='logout'),
    path('change-password/', auth_views.PasswordChangeView.as_view(template_name='./usuarios/change_password.html', success_url='/change-password-done/'), name='change_password'),
    path('change-password-done/', auth_views.PasswordChangeDoneView.as_view(template_name='./usuarios/change_password_done.html'), name='password_change_done'),
    path('produtos/', views.produtos, name='produtos'),
    path('produtos/aumentar/<int:produto_id>/', views.aumentar_quantidade, name='aumentar_quantidade'),    
    path('produtos/diminuir/<int:produto_id>/', views.diminuir_quantidade, name='diminuir_quantidade'),
    path('produtos/excluir/<int:produto_id>/', views.excluir_produto, name='excluir_produto'),
    path('sobre/', views.sobre, name='sobre'),
    path('contato/', views.contato, name='contato'),
    
]
