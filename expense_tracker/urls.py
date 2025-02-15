from django.contrib import admin
from django.urls import path
from tracker import views  # Import all views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.login_view, name='login'),  # Show login first
    path('home/', views.home, name='home'),  # Home after login
    path('logout/', views.logout_view, name='logout'),
    path('add-expense/', views.add_expense, name='add_expense'),
    path('add-income/', views.add_income, name='add_income'),
    path('view-expenses/', views.view_expenses, name='view_expenses'),
    path('set-budget/', views.set_budget, name='set_budget'),
]
