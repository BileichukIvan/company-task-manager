from django.test import TestCase

from manager.models import (
    Worker,
    Team,
    Tag,
    Position,
    TaskType,
    Project,
)
from manager.forms import (
    TaskForm,
    TaskSearchForm,
    WorkerCreationForm,
    WorkerForm,
    WorkerSearchForm,
    TeamForm,
    TeamSearchForm,
    TagForm,
    PositionForm,
)


class FormTestCase(TestCase):
    def setUp(self):
        # Set up initial data for tests.
        self.task_type = TaskType.objects.create(name="Bug")
        self.position = Position.objects.create(name="Developer")
        self.project = Project.objects.create(name="Project X", description="Test Project")
        self.worker = Worker.objects.create_user(
            username="worker",
            password="password",
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            position=self.position
        )
        self.team = Team.objects.create(name="Team A")
        self.team.members.add(self.worker)
        self.team.project.add(self.project)
        self.tag = Tag.objects.create(name="Urgent")


class TaskFormTest(FormTestCase):
    def test_valid_form(self):
        form_data = {
            "name": "Test Task",
            "description": "This is a test task.",
            "deadline": "2024-12-31",
            "is_completed": False,
            "priority": "high",
            "task_type": self.task_type.id,
            "assigned": [self.worker.id],
            "tags": [self.tag.id],
            "project": self.project.id
        }
        form = TaskForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        form_data = {
            "name": "",
            "description": "This is a test task.",
            "deadline": "2024-12-31",
            "is_completed": False,
            "priority": "high",
            "task_type": self.task_type.id,
            "assigned": [self.worker.id],
            "tags": [self.tag.id],
            "project": self.project.id
        }
        form = TaskForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)


class TaskSearchFormTest(FormTestCase):
    def test_valid_form(self):
        form_data = {"query": "Test", "show_my_tasks": True}
        form = TaskSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_empty_form(self):
        form = TaskSearchForm(data={})
        self.assertTrue(form.is_valid())


class WorkerFormTest(FormTestCase):
    def test_valid_worker_creation_form(self):
        form_data = {
            "username": "newworker",
            "password1": "UniquePassword!2024",
            "password2": "UniquePassword!2024",
            "first_name": "Jane",
            "last_name": "Smith",
            "email": "jane.smith@example.com",
            "position": self.position.id,
        }
        form = WorkerCreationForm(data=form_data)
        self.assertTrue(form.is_valid(), msg=form.errors)

    def test_invalid_worker_creation_form(self):
        form_data = {
            "username": "",
            "password1": "password",
            "password2": "password",
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "position": self.position.id
        }
        form = WorkerCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("username", form.errors)

    def test_valid_worker_form(self):
        form_data = {
            "username": "testworker",
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "position": self.position.id
        }
        form = WorkerForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_worker_form(self):
        form_data = {
            "username": "",
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "position": self.position.id
        }
        form = WorkerForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("username", form.errors)


class WorkerSearchFormTest(FormTestCase):
    def test_valid_form(self):
        form_data = {"username": "testworker"}
        form = WorkerSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_empty_form(self):
        form = WorkerSearchForm(data={})
        self.assertTrue(form.is_valid())


class TeamFormTest(FormTestCase):
    def test_valid_form(self):
        form_data = {
            "name": "Test Team",
            "members": [self.worker.id],
            "project": [self.project.id]
        }
        form = TeamForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        form_data = {"name": ""}
        form = TeamForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)


class TeamSearchFormTest(FormTestCase):
    def test_valid_form(self):
        form_data = {"name": "Test Team"}
        form = TeamSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_empty_form(self):
        form = TeamSearchForm(data={})
        self.assertTrue(form.is_valid())


class TagFormTest(FormTestCase):
    def test_valid_form(self):
        form_data = {"name": "Test Tag"}
        form = TagForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        form_data = {"name": ""}
        form = TagForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)


class PositionFormTest(FormTestCase):
    def test_valid_form(self):
        form_data = {"name": "Test Position"}
        form = PositionForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        form_data = {"name": ""}
        form = PositionForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)
