from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.template import loader
from .models import Todo
from django.utils import timezone

def index(request):
    todo_items = Todo.objects.order_by('-date_created')[:10]
    context = {
        'todo_items': todo_items,
    }
    return render(request, 'todos/index.html', context)


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
