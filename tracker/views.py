from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .models import Expense, Income, Category, Budget  # Import necessary models

# ✅ Login View (First Page)
def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')  # If already logged in, go to home

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')  # Redirect to home page after login
        else:
            return render(request, 'tracker/login.html', {'error': 'Invalid credentials'})

    return render(request, 'tracker/login.html')

# ✅ Logout View
def logout_view(request):
    logout(request)
    return redirect('login')  # Redirect to login page after logout

# ✅ Home View (Only accessible after login)
@login_required(login_url='/')
def home(request):
    return render(request, 'tracker/home.html')

# ✅ Add Expense View
@login_required(login_url='/')
def add_expense(request):
    if request.method == "POST":
        category_name = request.POST.get('category')
        amount = request.POST.get('amount')
        description = request.POST.get('description', '')

        category, created = Category.objects.get_or_create(name=category_name)

        Expense.objects.create(
            category=category,
            amount=amount,
            description=description,
            date=request.POST.get('date', None)
        )
        return render(request, 'tracker/add_expense.html', {'success': 'Expense added successfully!'})

    return render(request, 'tracker/add_expense.html')

# ✅ Add Income View
@login_required(login_url='/')
def add_income(request):
    if request.method == "POST":
        amount = request.POST.get('amount')
        description = request.POST.get('description', '')

        Income.objects.create(
            amount=amount,
            description=description,
            date=request.POST.get('date', None)
        )
        return render(request, 'tracker/add_income.html', {'success': 'Income added successfully!'})

    return render(request, 'tracker/add_income.html')

# ✅ View Expenses
@login_required(login_url='/')
def view_expenses(request):
    expenses = Expense.objects.all()
    return render(request, 'tracker/view_expenses.html', {'expenses': expenses})

# ✅ Set Budget
@login_required(login_url='/')
def set_budget(request):
    if request.method == "POST":
        category_name = request.POST.get('category')
        limit = request.POST.get('limit')

        category, created = Category.objects.get_or_create(name=category_name)

        Budget.objects.update_or_create(
            category=category,
            defaults={'limit': limit}
        )
        return render(request, 'tracker/set_budget.html', {'success': f'Budget for {category.name} set successfully!'})

    return render(request, 'tracker/set_budget.html')
