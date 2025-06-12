from django.urls import path
from . import views

app_name = 'expenses'

urlpatterns = [
    path('', views.home, name='home'),
    path('add-expense/', views.add_expense, name='add_expense'),
    path('expenses/', views.expense_list, name='expense_list'),
    path('reports/', views.reports, name='reports'),
    path('create-category/', views.create_category, name='create_category'),
    path('accounts/', views.account_list, name='account_list'),
    path('accounts/add/', views.add_account, name='add_account'),
    path('accounts/<int:pk>/edit/', views.edit_account, name='edit_account'),
    path('accounts/<int:pk>/delete/', views.delete_account, name='delete_account'),
]