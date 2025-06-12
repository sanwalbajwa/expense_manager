from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect
from django.contrib.auth import logout

def admin_logout(request):

    logout(request)
    return redirect('/admin/')

def user_logout(request):
    logout(request)
    return redirect('accounts:login')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin/logout/', admin_logout, name='admin_logout'),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('allauth.urls')),
    path('', include('expenses.urls')),
]