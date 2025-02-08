from django.urls import path
from . import views  # Import views from the tracker app

urlpatterns = [
    path('', views.home, name='home'),  # Home page
    path('add-expense/', views.add_expense, name='add_expense'),  # Add expense
    path('add-income/', views.add_income, name='add_income'),  # Add income
    path('view-expenses/', views.view_expenses, name='view_expenses'),  # View expenses
]
