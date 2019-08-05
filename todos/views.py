from django.shortcuts import render, get_object_or_404, redirect
from .models import Todo, Category
import dateutil.parser as parser
from django.core.mail import send_mail
from django.http import HttpResponse
from datetime import datetime


def index(request):
    todo_items = Todo.objects.order_by('-date_created')[:10]
    category_items = Category.objects.all()

    current_date_time = datetime.now()
    dt_string = current_date_time.strftime("%m/%d/%Y %I:%M %p")
    splited_dt_string = dt_string.split(" ")

    context = {
        'todo_items': todo_items,
        'category_items': category_items,
        'hide_side_bar' : False,
        'current_date': splited_dt_string[0] + str().join(" ") + splited_dt_string[1] + str().join(" ") + splited_dt_string[2]
    }

    return render(request, 'todos/index.html', context)


def addTodo(request):
    if request.POST['email_notification']:
        receiver_email = request.POST['email_notification']
        sendEmail(request, receiver_email)

    new_item = Todo(todo_text = request.POST['todo_text'],
                    date_created = (parser.parse(request.POST['date_created'])).isoformat(),
                    due_date = (parser.parse(request.POST['due_date'])).isoformat(),
                    category_id = request.POST['todo_category'],
                    email_notification = request.POST['email_notification'])

    print((parser.parse(request.POST['due_date'])).isoformat())
    new_item.save()

    category_id = request.POST['todo_category']
    category = get_object_or_404(Category, pk=category_id)
    category.todo_count += 1
    category.save()
    return redirect("/todos")


def addCategory(request):
    new_category = Category(category_name = request.POST['category_name'])
    new_category.save()
    return redirect("/todos")


def edit(request, todo_id):
    if request.path == "/todos/" + str(todo_id) + "/edit/":
        hide_side_bar = True

    todo = get_object_or_404(Todo, pk=todo_id)
    due_date = todo.due_date.strftime("%m/%d/%Y %I:%M %p")
    splited_due_date_string = due_date.split(" ")

    context = {
        'todo_id' : todo_id,
        'todo_text' : todo.todo_text,
        'due_date': splited_due_date_string[0] + str().join(" ") + splited_due_date_string[1] + str().join(" ") + splited_due_date_string[2],
        'hideSideBar' : hide_side_bar
    }
    return render(request, 'todos/edit.html', context)


def update(request, todo_id):

    edited_item = request.POST['todo_text']
    edited_due_date = (parser.parse(request.POST['due_date'])).isoformat()
    todo = get_object_or_404(Todo, pk=todo_id)
    todo.todo_text = edited_item
    todo.due_date = edited_due_date
    todo.save()
    return redirect("/todos")


def delete(request, todo_id):
    todo = get_object_or_404(Todo, pk=todo_id)
    Todo.delete(todo)

    category = get_object_or_404(Category, pk= todo.category_id)
    category.todo_count -= 1
    category.save()
    return redirect("/todos")


def sendEmail(request, receiver_email):

    email_body = """
    You have added a new todo_item.
    You can edit and delete the todo_item anytime.
    You will receive an email once it is expired!"""

    todo_item_expire = """
    Your todo_item has been expired
    Your todo_item has been expired
    Your todo_item has been expired"""

    print(todo_item_expire)

    send_mail(
        'Todo_Notification',
        email_body,
        'noreply@todo_application.ca',
        [receiver_email],
        fail_silently=False,
    )

    return HttpResponse('Mail successfully sent')