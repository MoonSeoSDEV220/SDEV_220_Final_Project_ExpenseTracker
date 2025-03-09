from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Expense, Income, Category, Budget
from datetime import datetime
from decimal import Decimal
import io
import base64
from collections import defaultdict

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password")
            return render(request, 'tracker/login.html')

    return render(request, 'tracker/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def home(request):
    return render(request, 'tracker/home.html')

@login_required(login_url='login')
def add_expense(request):
    categories = Category.objects.all()
    
    if request.method == "POST":
        category_id = request.POST.get('category')
        new_category_name = request.POST.get('new_category')
        amount = request.POST.get('amount')
        date = request.POST.get('date')

        if not category_id and not new_category_name:
            messages.error(request, "Please select an existing category or add a new one.")
            return render(request, 'tracker/add_expense.html', {'categories': categories})

        if new_category_name:
            category, created = Category.objects.get_or_create(name=new_category_name)
        else:
            try:
                category = get_object_or_404(Category, id=int(category_id))
            except ValueError:
                messages.error(request, "Invalid category selected.")
                return render(request, 'tracker/add_expense.html', {'categories': categories})

        try:
            amount = Decimal(amount)
            if amount <= 0:
                messages.error(request, "Amount must be greater than zero.")
                return render(request, 'tracker/add_expense.html', {'categories': categories})

            date = datetime.strptime(date, "%Y-%m-%d").date()
        except (ValueError, TypeError):
            messages.error(request, "Invalid date format. Please use YYYY-MM-DD.")
            return render(request, 'tracker/add_expense.html', {'categories': categories})

        Expense.objects.create(user=request.user, category=category, amount=amount, description=description, date=date)

        messages.success(request, "Expense added successfully!")
        return render(request, 'tracker/add_expense.html', {'categories': categories})

    return render(request, 'tracker/add_expense.html', {'categories': categories})

@login_required(login_url='login')
def add_income(request):
    if request.method == "POST":
        amount = request.POST.get('amount')
        date_value = request.POST.get('date')
        description = request.POST.get('description', '')

        if not amount or not date_value:
            messages.error(request, "All fields are required.")
            return render(request, 'tracker/add_income.html')

        try:
            amount = Decimal(amount)
            if amount <= 0:
                messages.error(request, "Income amount must be greater than zero.")
                return render(request, 'tracker/add_income.html')

            date_value = datetime.strptime(date_value, "%Y-%m-%d").date()
        except (ValueError, TypeError):
            messages.error(request, "Invalid date format. Please use YYYY-MM-DD.")
            return render(request, 'tracker/add_income.html')

        Income.objects.create(user=request.user, amount=amount, description=description, date=date_value)

        messages.success(request, "Income added successfully!")
        return render(request, 'tracker/add_income.html')

    return render(request, 'tracker/add_income.html')

@login_required(login_url='login')
def set_budget(request):
    categories = Category.objects.all()
    
    if request.method == "POST":
        category_name = request.POST.get("category")
        limit = request.POST.get('limit')
        month_input = request.POST.get('month')

        if not month_input: 
            messages.error(request, "Please select a month.")
            return render(request, 'tracker/set_budget.html', {'categories': categories})

        try:
            month = datetime.strptime(month_input, "%Y-%m").date()  # ✅ Convert safely
        except ValueError:
            messages.error(request, "Invalid month format. Please use YYYY-MM.")
            return render(request, 'tracker/set_budget.html', {'categories': categories})

        new_category = request.POST.get("new_category")
        if (not category_name and not new_category) or not limit or not month:
            messages.error(request, "Please select an existing category or add a new one.")
            return render(request, 'tracker/set_budget.html', {'categories': categories})
        if new_category:
            category, created = Category.objects.get_or_create(name=new_category)
        else:
            category = get_object_or_404(Category, name=category_name)

        try:
            limit = Decimal(limit)
            if limit <= 0:
                messages.error(request, "Budget limit must be greater than zero.")
                return render(request, 'tracker/set_budget.html', {'categories': categories})
        except (ValueError, TypeError):
            messages.error(request, "Invalid amount format.")
            return render(request, 'tracker/set_budget.html', {'categories': categories})

        Budget.objects.update_or_create(user=request.user, category=category, month=month, defaults={'limit': limit})

        messages.success(request, f"Budget for {category.name} set successfully!")
        return render(request, 'tracker/set_budget.html', {'categories': categories})

    return render(request, 'tracker/set_budget.html', {'categories': categories})

@login_required(login_url='login')
def view_summary(request):
    expenses = Expense.objects.filter(user=request.user).order_by('-date')
    incomes = Income.objects.filter(user=request.user).order_by('-date')
    budgets = Budget.objects.filter(user=request.user).order_by('-month')

    return render(request, 'tracker/view_summary.html', {
        'expenses': expenses,
        'incomes': incomes,
        'budgets': budgets
    })

@login_required(login_url='login')
def view_analytics(request):
    expenses = Expense.objects.filter(user=request.user)
    incomes = Income.objects.filter(user=request.user)
    budgets = Budget.objects.filter(user=request.user)

    expense_data = defaultdict(Decimal)
    budget_data = defaultdict(Decimal)
    category_totals = defaultdict(Decimal)

    income_total = sum(income.amount for income in incomes) if incomes.exists() else Decimal("0.0")
    expense_total = sum(expense.amount for expense in expenses) if expenses.exists() else Decimal("0.0")

    for expense in expenses:
        month_year = expense.date.strftime("%m-%Y")
        expense_data[month_year] += expense.amount
        category_totals[expense.category.name] += expense.amount

    for budget in budgets:
        budget_data[budget.category.name] = budget.limit

    expense_dates = sorted(expense_data.keys())
    expense_amounts = [float(expense_data[date]) for date in expense_dates]
    budget_amounts = [float(budget_data.get(date, Decimal("0.0"))) for date in expense_dates]

    fig1, ax1 = plt.subplots(figsize=(8, 5))
    ax1.plot(expense_dates, expense_amounts, marker='o', linestyle='-', color='b')
    ax1.set_title('Spending Trend Over Time')
    ax1.set_xlabel('Month-Year')
    ax1.set_ylabel('Amount Spent (USD)')
    ax1.tick_params(axis='x', rotation=45)

    buffer1 = io.BytesIO()
    plt.savefig(buffer1, format='png')
    buffer1.seek(0)
    spending_trend_chart = base64.b64encode(buffer1.getvalue()).decode('utf-8')
    buffer1.close()
    plt.close(fig1)

    fig2, ax2 = plt.subplots(figsize=(8, 5))
    ax2.plot(expense_dates, budget_amounts, marker='o', linestyle='-', color='green', label='Budget')
    ax2.plot(expense_dates, expense_amounts, linestyle='-', label='Expenses')
    ax2.set_title('Budget vs. Expenses')
    ax2.set_xlabel('Month-Year')
    ax2.set_ylabel('Amount (USD)')
    ax2.legend()
    ax2.tick_params(axis='x', rotation=45)

    buffer2 = io.BytesIO()
    plt.savefig(buffer2, format='png')
    buffer2.seek(0)
    budget_vs_expenses_chart = base64.b64encode(buffer2.getvalue()).decode('utf-8')
    buffer2.close()
    plt.close(fig2)

    fig3, ax3 = plt.subplots(figsize=(5, 5))
    if income_total > Decimal("0.0") or expense_total > Decimal("0.0"):
        ax3.pie([float(income_total), float(expense_total)], labels=['Income', 'Expenses'], autopct='%1.1f%%', colors=['blue', 'red'])
    else:
        ax3.text(0, 0, "No data available", ha='center', va='center')
    ax3.set_title('Income vs. Expenses')

    buffer3 = io.BytesIO()
    plt.savefig(buffer3, format='png')
    buffer3.seek(0)
    income_vs_expenses_chart = base64.b64encode(buffer3.getvalue()).decode('utf-8')
    buffer3.close()
    plt.close(fig3)

    fig4, ax4 = plt.subplots(figsize=(5, 5))
    if category_totals:
        ax4.pie([float(value) for value in category_totals.values()], 
            labels=category_totals.keys(), 
            autopct='%1.1f%%')
    else:
        ax4.text(0, 0, "No data available", ha='center', va='center')
    ax4.set_title('Expense Breakdown by Category')

    buffer4 = io.BytesIO()
    plt.savefig(buffer4, format='png')
    buffer4.seek(0)
    expense_breakdown_chart = base64.b64encode(buffer4.getvalue()).decode('utf-8')  # ✅ This was missing
    buffer4.close()
    plt.close(fig4)


    return render(request, 'tracker/view_analytics.html', {
    'spending_trend_chart': spending_trend_chart,
    'budget_vs_expenses_chart': budget_vs_expenses_chart,
    'income_vs_expenses_chart': income_vs_expenses_chart,
    'expense_breakdown_chart': expense_breakdown_chart,
})

