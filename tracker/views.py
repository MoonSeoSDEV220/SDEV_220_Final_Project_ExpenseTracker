from django.shortcuts import render

# Add Expense view
def add_expense(request):
    return render(request, 'tracker/add_expense.html')  # Render the add_expense.html template

# Home view
def home(request):
    return render(request, 'tracker/home.html')  # Render the home.html template
