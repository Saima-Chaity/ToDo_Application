from django.shortcuts import render, get_object_or_404, redirect
from .models import Todo, Category, NotificationTime
import dateutil.parser as parser
from django.core.mail import send_mail
from django.http import HttpResponse
from datetime import datetime, time
import sqlite3
import time, traceback
import threading


def index(request):
    todo_items = Todo.objects.order_by('-due_date')[:10]
    category_items = Category.objects.all()
    notification_time = NotificationTime.objects.all()

    current_date_time = datetime.now()
    dt_string = current_date_time.strftime("%m/%d/%Y %I:%M %p")
    splited_dt_string = dt_string.split(" ")

    context = {
        'todo_items': todo_items,
        'category_items': category_items,
        'notification_time' : notification_time,
        'hide_side_bar' : False,
        'current_date': splited_dt_string[0] + str().join(" ") + splited_dt_string[1] + str().join(" ") + splited_dt_string[2]
    }
    return render(request, 'todos/index.html', context)


def addTodo(request):
    receiver_email = ""
    notification_time = "not available"
    if request.POST['email_notification']:
        receiver_email = request.POST['email_notification']

    if request.POST['todo_notification_time']:
        notification_time = request.POST['todo_notification_time']

    sendEmail(request, receiver_email, notification_time)

    new_item = Todo(todo_text = request.POST['todo_text'],
                    date_created = (parser.parse(request.POST['date_created'])).isoformat(),
                    due_date = (parser.parse(request.POST['due_date'])).isoformat(),
                    category_id = request.POST['todo_category'],
                    email_notification = request.POST['email_notification'],
                    notification_time = notification_time)

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


def sendEmail(request, receiver_email, notification_time):

    email_body = """
    You have added a new todo_item.
    You can edit and delete the todo_item anytime.
    Your item will expire in """ + str(notification_time) + "!"

    send_mail(
        'Todo_Notification',
        email_body,
        'noreply@todo_application.ca',
        [receiver_email],
        fail_silently=False,
    )
    return HttpResponse('Mail successfully sent')


def check_time(delay, task):
  next_time = time.time() + delay
  while True:
    time.sleep(max(0, next_time - time.time()))
    try:
      task()
    except Exception:
      traceback.print_exc()
    # skip tasks if we are behind schedule:
    next_time += (time.time() - next_time) // delay * delay + delay

def is_expired():
    connection = sqlite3.connect('db.sqlite3')
    cursor = connection.cursor()
    cursor.execute(" SELECT * FROM todos_todo where email_notification != '' AND notification_time != 'None' AND sent_reminder == 'False' ")
    rows = cursor.fetchall()
    todo_notify_time = 0

    for row in rows:
        todo_item_id = row[0]
        due_date_in_ms = int(datetime.fromisoformat(row[3]).timestamp() * 1000)
        current_date = int(datetime.now().timestamp() * 1000)
        splited_notification_time = str(row[6]).split(" ")
        receiver_email = row[5]
        sent_reminder = row[7]
        date_in_pst = due_date_in_ms - (7 * 60 * 60 * 1000)
        time_remaining = date_in_pst - current_date

        if splited_notification_time[0] != "None":
            if splited_notification_time[1] == "minutes":
                todo_notify_time = int((splited_notification_time[0])) * 60 * 1000
            elif splited_notification_time[1] == "hours":
                todo_notify_time = int((splited_notification_time[0])) * 60 * 60 * 1000
            elif splited_notification_time[1] == "day":
                todo_notify_time = int((splited_notification_time[0])) * 60 * 60 * 24 * 1000

        if time_remaining <= todo_notify_time:
            todo_item_expire = "Your todo_item name - " + str(row[1]) +  " will expire in " + str(row[6]) + "! "

            send_mail(
                'Todo_Notification',
                todo_item_expire,
                'noreply@todo_application.ca',
                [receiver_email],
                fail_silently=False,
            )

            selected_todo_item = get_object_or_404(Todo, pk=int(todo_item_id))
            selected_todo_item.sent_reminder = "True"
            selected_todo_item.save()

threading.Thread(target=lambda: check_time(1, is_expired)).start()