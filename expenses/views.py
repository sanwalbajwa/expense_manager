from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Sum

from accounts import models

from .forms import ExpenseForm, AccountForm
from .models import Expense, Category,Account

@login_required
def home(request):
    # Get current date
    current_date = timezone.now()
    
    # Calculate total expenses
    total_expenses = Expense.objects.filter(user=request.user).aggregate(
        total=Sum('amount')
    )['total'] or 0
    
    # Calculate monthly expenses
    monthly_expenses = Expense.objects.filter(
        user=request.user,
        date__month=current_date.month,
        date__year=current_date.year
    ).aggregate(total=Sum('amount'))['total'] or 0
    
    # Get total categories
    total_categories = Category.objects.filter(user=request.user).count()
    
    # Get recent expenses
    recent_expenses = Expense.objects.filter(user=request.user).order_by('-date')[:5]
    
    context = {
        'current_date': current_date,
        'total_expenses': total_expenses,
        'monthly_expenses': monthly_expenses,
        'total_categories': total_categories,
        'recent_expenses': recent_expenses,
    }
    
    return render(request, 'expenses/home.html', context)

@login_required
def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST, user=request.user)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            messages.success(request, 'Expense added successfully!')
            return redirect('expenses:expense_list')
    else:
        form = ExpenseForm(user=request.user)
    
    return render(request, 'expenses/add_expense.html', {'form': form})

@login_required
def expense_list(request):
    expenses = Expense.objects.filter(user=request.user).order_by('-date')
    return render(request, 'expenses/expense_list.html', {'expenses': expenses})

@login_required
def reports(request):
    # Temporary placeholder
    return render(request, 'expenses/reports.html')

@login_required
def create_category(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description', '')
        
        # Validate category name
        if not name:
            messages.error(request, 'Category name is required.')
            return render(request, 'expenses/create_category.html')
        
        # Check for duplicate categories
        if Category.objects.filter(name__iexact=name, user=request.user).exists():
            messages.error(request, 'A category with this name already exists.')
            return render(request, 'expenses/create_category.html')
        
        # Create category
        Category.objects.create(
            name=name, 
            description=description, 
            user=request.user
        )
        messages.success(request, f'Category "{name}" created successfully!')
        return redirect('expenses:category_list')
    
    return render(request, 'expenses/create_category.html')

@login_required
def account_list(request):
    accounts = Account.objects.filter(user=request.user)
    
    # Calculate balance for each account
    account_details = []
    for account in accounts:
        total_expenses = account.expenses.aggregate(total=Sum('amount'))['total'] or 0
        account_details.append({
            'account': account,
            'total_balance': account.initial_balance - total_expenses
        })
    
    return render(request, 'expenses/account_list.html', {
        'account_details': account_details
    })

@login_required
def add_account(request):
    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.user = request.user
            account.save()
            messages.success(request, f'Account "{account.name}" added successfully!')
            return redirect('expenses:account_list')
    else:
        form = AccountForm()
    
    return render(request, 'expenses/add_account.html', {'form': form})

@login_required
def edit_account(request, pk):
    account = get_object_or_404(Account, pk=pk, user=request.user)
    
    if request.method == 'POST':
        form = AccountForm(request.POST, instance=account)
        if form.is_valid():
            form.save()
            messages.success(request, f'Account "{account.name}" updated successfully!')
            return redirect('expenses:account_list')
    else:
        form = AccountForm(instance=account)
    
    return render(request, 'expenses/edit_account.html', {'form': form})

@login_required
def delete_account(request, pk):
    account = get_object_or_404(Account, pk=pk, user=request.user)
    
    if request.method == 'POST':
        account.delete()
        messages.success(request, f'Account "{account.name}" deleted successfully!')
        return redirect('expenses:account_list')
    
    return render(request, 'expenses/delete_account.html', {'account': account})