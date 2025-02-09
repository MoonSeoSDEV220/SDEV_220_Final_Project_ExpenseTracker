from django.shortcuts import render
from .models import Expense, Income, Category, Budget

# Home view
def home(request):
    return render(request, 'tracker/home.html')  # Render the home page

# Add expense view
def add_expense(request):
    if request.method == "POST":
        category_name = request.POST.get('category')
        amount = request.POST.get('amount')
        description = request.POST.get('description', '')

        # Check if category exists
        category, created = Category.objects.get_or_create(name=category_name)

        # Save the expense
        Expense.objects.create(
            category=category,
            amount=amount,
            description=description,
            date=request.POST.get('date', None)  # Add date
        )
        return render(request, 'tracker/add_expense.html', {'success': 'Expense added successfully!'})

    return render(request, 'tracker/add_expense.html')  # Render the add expense page

# Add income view
def add_income(request):
    if request.method == "POST":
        amount = request.POST.get('amount')
        description = request.POST.get('description', '')

        # Save the income
        Income.objects.create(
            amount=amount,
            description=description,
            date=request.POST.get('date', None)  # Add date
        )
        return render(request, 'tracker/add_income.html', {'success': 'Income added successfully!'})

    return render(request, 'tracker/add_income.html')  # Render the add income page

# View expenses view
def view_expenses(request):
    expenses = Expense.objects.all()  # Fetch all expenses
    return render(request, 'tracker/view_expenses.html', {'expenses': expenses})

# Set budget view
def set_budget(request):
    if request.method == "POST":
        category_name = request.POST.get('category')
        limit = request.POST.get('limit')

        # Check if category exists
        category, created = Category.objects.get_or_create(name=category_name)

        # Save or update the budget
        Budget.objects.update_or_create(
            category=category,
            defaults={'limit': limit}
        )
        return render(request, 'tracker/set_budget.html', {'success': f'Budget for {category.name} set successfully!'})

    return render(request, 'tracker/set_budget.html')  # Render the set budget page
