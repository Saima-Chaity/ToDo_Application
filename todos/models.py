from django.db import models
import datetime

class Todo(models.Model):
    todo_text = models.CharField(max_length=1000)
    date_created = models.DateTimeField(default=datetime.datetime.now)
    due_date = models.DateTimeField('due_date', null=True)

    def __str__(self):
        return self.todo_text


