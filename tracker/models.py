from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

# Category model
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)  # Name of the category
    description = models.TextField(blank=True, null=True)  # Optional description

    def __str__(self):
        return self.name

# Expense model
class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to the user
    category = models.ForeignKey(Category, on_delete=models.CASCADE)  # Link to category
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Amount spent
    date = models.DateField()  # Date of expense
    description = models.TextField(blank=True, null=True)  # Optional description

    def __str__(self):
        return f"{self.user.username} - {self.category.name} - {self.amount}"

# Income model
class Income(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to the user
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Amount earned
    date = models.DateField()  # Date of income
    description = models.TextField(blank=True, null=True)  # Optional description

    def __str__(self):
        return f"{self.user.username} - {self.amount}"

# Budget model
class Budget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to the user
    category = models.ForeignKey(Category, on_delete=models.CASCADE)  # Link to category
    limit = models.DecimalField(max_digits=10, decimal_places=2)  # Budget limit

    def __str__(self):
        return f"{self.user.username} - {self.category.name} - {self.limit}"
