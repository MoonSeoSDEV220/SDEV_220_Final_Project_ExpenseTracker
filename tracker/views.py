from django.shortcuts import render, redirect
from django.db.models import Sum
from django.contrib import messages
from datetime import date
from .models import Expense, Income, Category, Budget
from django.contrib.auth.models import User  # Replace this with request.user when authentication is added

# Home view
def home(request):
    return render(request, 'tracker/home.html')  # Render the home page

# Add expense view with budget validation
def add_expense(request):
    if request.method == "POST":
        # Get form data
        category_name = request.POST.get('category')
        amount = float(request.POST.get('amount'))
        description = request.POST.get('description', '')

        # Check if category exists
        category, created = Category.objects.get_or_create(name=category_name)

        # Check if a budget exists for the category
        budget = Budget.objects.filter(user=User.objects.first(), category=category).first()

        if budget:
            # Calculate total expenses for this category
            total_expenses = Expense.objects.filter(user=User.objects.first(), category=category).aggregate(Sum('amount'))['amount__sum'] or 0
            if total_expenses + amount > budget.limit:
                messages.error(request, f"Adding this expense exceeds the budget limit for {category.name}!")
                return redirect('add_expense')

        # Save the expense
        Expense.objects.create(
            user=User.objects.first(),  # Temporary: Replace with actual logged-in user
            category=category,
            amount=amount,
            description=description,
            date=date.today()
        )
        messages.success(request, "Expense added successfully!")
        return redirect('home')

    return render(request, 'tracker/add_expense.html')  # Render the add expense page

# Add income view
def add_income(request):
    if request.method == "POST":
        # Get form data
        amount = float(request.POST.get('amount'))
        description = request.POST.get('description', '')

        # Save the income
        Income.objects.create(
            user=User.objects.first(),  # Temporary: Replace with actual logged-in user
            amount=amount,
            description=description,
            date=date.today()
        )
        messages.success(request, "Income added successfully!")
        return redirect('home')

    return render(request, 'tracker/add_income.html')  # Render the add income page

# View expenses view
def view_expenses(request):
    # Retrieve all expenses for the current user (replace with actual logged-in user)
    expenses = Expense.objects.filter(user=User.objects.first())
    context = {'expenses': expenses}
    return render(request, 'tracker/view_expenses.html', context)  # Render the view expenses page

# Set budget view
def set_budget(request):
    if request.method == "POST":
        category_name = request.POST.get('category')
        limit = float(request.POST.get('limit'))

        # Check if category exists
        category, created = Category.objects.get_or_create(name=category_name)

        # Create or update the budget
        budget, created = Budget.objects.update_or_create(
            user=User.objects.first(),  # Temporary: Replace with actual logged-in user
            category=category,
            defaults={'limit': limit}
        )

        messages.success(request, f"Budget for {category.name} set to {limit} successfully!")
        return redirect('home')

    return render(request, 'tracker/set_budget.html')  # Render the set budget page
