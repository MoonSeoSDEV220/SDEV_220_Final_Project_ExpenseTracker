from django.urls import path
from tracker import views

urlpatterns = [
    path('', views.login_view, name='login'),  # Login page
    path('logout/', views.logout_view, name='logout'),  # Logout
    path('home/', views.home, name='home'),
    path('add-expense/', views.add_expense, name='add_expense'),
    path('add-income/', views.add_income, name='add_income'),
    path('set-budget/', views.set_budget, name='set_budget'),
    path('view-summary/', views.view_summary, name='view_summary'),
    path('view-analytics/', views.view_analytics, name='view_analytics'),
]
