from django.db import models
import datetime


class Category(models.Model):
    category_name = models.CharField(max_length=100)
    todo_count = models.IntegerField(default=0)

    def __str__(self):
        return self.category_name


class Todo(models.Model):
    todo_text = models.CharField(max_length=1000)
    date_created = models.DateTimeField(default=datetime.datetime.now)
    due_date = models.DateTimeField('due_date', null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.todo_text
