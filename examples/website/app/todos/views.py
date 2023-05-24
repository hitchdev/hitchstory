from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from .models import Todo
from django.http import HttpResponseRedirect
from textblob import TextBlob
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


def correct_spelling(text):
    blob = TextBlob(text)
    corrected = str(blob.correct())
    if corrected != text:
        return suggest_spelling(text)
    else:
        return corrected


def suggest_spelling(text):
    blob = TextBlob(text)
    suggestion = str(blob.correct())
    return suggestion


@method_decorator(login_required, name="dispatch")
class IndexView(generic.ListView):
    template_name = "todos/index.html"
    context_object_name = "todo_list"

    def get_queryset(self):
        """Return all the latest todos."""
        return Todo.objects.order_by("-created_at")


@login_required
def add(request):
    title = request.POST["title"]
    if correct_spelling(title) != title:
        return render(
            request,
            "todos/index.html",
            {"error_message": "Did you mean '{}'?".format(correct_spelling(title))},
        )
    else:
        Todo.objects.create(title=title)
        return redirect("todos:index")


@login_required
def delete(request, todo_id):
    todo = get_object_or_404(Todo, pk=todo_id)
    todo.delete()

    return redirect("todos:index")


@login_required
def update(request, todo_id):
    todo = get_object_or_404(Todo, pk=todo_id)
    isCompleted = request.POST.get("isCompleted", False)
    if isCompleted == "on":
        isCompleted = True

    todo.isCompleted = isCompleted

    todo.save()
    return redirect("todos:index")
