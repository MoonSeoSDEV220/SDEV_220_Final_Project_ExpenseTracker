from django.urls import path # type: ignore
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Home page
    path('add-expense/', views.add_expense, name='add_expense'),  # Add expense
    path('add-income/', views.add_income, name='add_income'),  # Add income
    path('view-expenses/', views.view_expenses, name='view_expenses'),  # View expenses
    path('set-budget/', views.set_budget, name='set_budget'),  # Set budget
]
