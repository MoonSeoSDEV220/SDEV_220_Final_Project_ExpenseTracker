from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Category, Expense, Income, Budget

# Register your models here
admin.site.register(Category)
admin.site.register(Expense)
admin.site.register(Income)
admin.site.register(Budget)
