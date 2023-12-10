from django.test import TestCase
from unittest.mock import MagicMock, patch
from django.contrib.auth.models import User
from django.test.client import RequestFactory
from django.shortcuts import get_object_or_404
from todos.views import delete


class DeleteTodo(TestCase):
    @patch('todos.views.get_object_or_404')
    def test_delete(self, get_object_or_404):
        user = User.objects.create_user(
            username="u", email="e", password="pwd"
        )
        request = RequestFactory().get("/delete/")
        request.user = user
        delete(request, 1)
