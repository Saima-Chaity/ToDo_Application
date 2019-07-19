from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template import loader
from .models import Todo

def index(request):
    todo_items = Todo.objects.order_by('-date_created')[:10]
    context = {
        'todo_items': todo_items,
    }
    return render(request, 'todos/index.html', context)


def edit(request, todo_id):
    todo = get_object_or_404(Todo, pk=todo_id)
    context = {
        'todo_text' : todo.todo_text,
        'date_created': todo.date_created
    }
    return render(request, 'todos/edit.html', context)