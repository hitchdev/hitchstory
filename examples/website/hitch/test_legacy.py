from test_integration import Engine
from playwright.sync_api import expect
from pytest import fixture
from os import getenv
import nest_asyncio

nest_asyncio.apply()


@fixture
def my_website():
    return Engine(
        rewrite=getenv("STORYMODE", "") == "rewrite",
        vnc=getenv("STORYMODE", "") == "vnc",
        coverage=getenv("STORYMODE", "") == "coverage",
        timeout=10.0,
    )


def test_add_and_retrieve_todo(my_website):
    """Demonstates the normal way UI tests are written."""
    my_website._given = {"browser": "chromium"}
    my_website.set_up()
    page = my_website._page

    try:
        # Arrange
        page.goto("http://localhost:8000/login")
        page.get_by_test_id("username").fill("admin")
        page.get_by_test_id("password").fill("password")
        page.get_by_test_id("submit").click()

        # Act
        page.get_by_test_id("todo-text").fill("Add bread")
        page.get_by_test_id("add").click()

        # Assert
        expect(page.locator(".test-todo-list-item").nth(0)).to_contain_text("Add bread")
    finally:
        my_website.tear_down()
