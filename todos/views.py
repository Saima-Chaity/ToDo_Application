from django.shortcuts import render, get_object_or_404, redirect
from .models import Todo
import dateutil.parser as parser


def index(request):
    todo_items = Todo.objects.order_by('-date_created')[:10]
    context = {
        'todo_items': todo_items,
    }
    return render(request, 'todos/index.html', context)


def addTodo(request):
    new_item = Todo(todo_text = request.POST['todo_text'], date_created = (parser.parse(request.POST['date_created'])).isoformat())
    new_item.save()
    return redirect("/todos")


def edit(request, todo_id):
    todo = get_object_or_404(Todo, pk=todo_id)
    context = {
        'todo_id' : todo_id,
        'todo_text' : todo.todo_text,
        'date_created': todo.date_created
    }
    return render(request, 'todos/edit.html', context)


def update(request, todo_id):

    edited_item = request.POST['todo_text']
    todo = get_object_or_404(Todo, pk=todo_id)
    todo.todo_text = edited_item
    todo.save()
    return redirect("/todos")


def delete(request, todo_id):
    todo = get_object_or_404(Todo, pk=todo_id)
    Todo.delete(todo)
    return redirect("/todos")