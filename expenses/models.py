from django.db import models
from django.contrib.auth.models import User

class Account(models.Model):
    ACCOUNT_TYPES = [
        ('CASH', 'Cash'),
        ('BANK', 'Bank Account'),
        ('DIGITAL', 'Digital Wallet'),
        ('CREDIT', 'Credit Card'),
        ('INVESTMENT', 'Investment Account'),
        ('OTHER', 'Other')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='accounts')
    name = models.CharField(max_length=100)
    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPES, default='CASH')
    initial_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    def get_total_balance(self):
        # Calculate total balance including expenses and incomes
        total_expenses = self.expenses.aggregate(total=models.Sum('amount'))['total'] or 0
        total_incomes = self.incomes.aggregate(total=models.Sum('amount'))['total'] or 0
        return self.initial_balance - total_expenses + total_incomes

class Category(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='categories')

    def __str__(self):
        return self.name

class Expense(models.Model):
    PAYMENT_METHODS = [
        ('CASH', 'Cash'),
        ('CREDIT', 'Credit Card'),
        ('DEBIT', 'Debit Card'),
        ('BANK_TRANSFER', 'Bank Transfer'),
        ('OTHER', 'Other')
    ]

    CURRENCY_CHOICES = [
        ('USD', 'US Dollar ($)'),
        # Add other currencies if needed
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='expenses')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='USD')
    date = models.DateField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='expenses')
    description = models.TextField(blank=True, null=True)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS, default='CASH')
    account = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, related_name='expenses')

    def __str__(self):
        return f"{self.get_currency_display()} {self.amount} - {self.category} on {self.date}"