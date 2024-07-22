from django.test import TestCase
from manager.models import TaskType, Position, Tag, Project, Team, Task
from django.contrib.auth import get_user_model
from datetime import date

User = get_user_model()


class ModelTestCase(TestCase):
    def setUp(self):
        # Common setup for all tests
        self.position = Position.objects.create(name="Developer")
        self.worker = User.objects.create_user(
            username="worker",
            password="password",
            first_name="John",
            last_name="Doe",
            position=self.position
        )
        self.task_type = TaskType.objects.create(name="Bug Fix")
        self.tag = Tag.objects.create(name="Critical")
        self.project = Project.objects.create(
            name="Project C",
            description="Description of Project C"
        )
        self.team = Team.objects.create(name="Team Alpha")
        self.team.members.add(self.worker)
        self.team.project.add(self.project)

    def test_task_type_str(self):
        task_type = TaskType.objects.create(name="Development")
        self.assertEqual(str(task_type), "Development")

    def test_position_str(self):
        position = Position.objects.create(name="Manager")
        self.assertEqual(str(position), "Manager")

    def test_tag_str(self):
        tag = Tag.objects.create(name="Urgent")
        self.assertEqual(str(tag), "Urgent")

    def test_project_str(self):
        self.assertEqual(str(self.project), "Project C")

    def test_team_str(self):
        self.assertEqual(str(self.team), "Team Alpha")

    def test_team_members_and_projects(self):
        # Test team members and projects
        self.assertIn(self.worker, self.team.members.all())
        self.assertIn(self.project, self.team.project.all())

    def test_worker_str(self):
        self.assertEqual(str(self.worker), "worker (John, Doe)")

    def test_task_str_and_associations(self):
        task = Task.objects.create(
            name="Fix Login Issue",
            description="Fix the login issue in the application",
            deadline=date.today(),
            priority="high",
            task_type=self.task_type,
            project=self.project
        )
        task.assigned.add(self.worker)
        task.tags.add(self.tag)

        # Test string representation
        self.assertEqual(str(task), "Fix Login Issue")

        # Test task assigned workers and tags
        self.assertIn(self.worker, task.assigned.all())
        self.assertIn(self.tag, task.tags.all())
