from django.db import models


class Todo(models.Model):
    todo_text = models.CharField(max_length=1000)
    date_created = models.DateTimeField('date_created')

    def __str__(self):
        return self.todo_text


