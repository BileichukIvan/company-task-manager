from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from datetime import datetime, timedelta

from company_task_manager.manager.models import (
    Task,
    Worker,
    Project,
    Team,
    Tag,
    Position,
    TaskType,
)


User = get_user_model()


class BaseTestCase(TestCase):
    def setUp(self):
        self.position = Position.objects.create(name="Developer")
        self.user = User.objects.create_user(
            username="testuser",
            password="password",
            position=self.position
        )
        self.client.login(username="testuser", password="password")

        self.worker = Worker.objects.create_user(
            username="worker",
            password="password",
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            position=self.position
        )
        self.project = Project.objects.create(
            name="Project X",
            description="Test Project"
        )
        self.task_type = TaskType.objects.create(name="Bug")
        self.task = Task.objects.create(
            name="Test Task",
            description="This is a test task.",
            project=self.project,
            task_type=self.task_type,
            deadline=datetime.now() + timedelta(days=7)  # Example deadline
        )
        self.tag = Tag.objects.create(name="Urgent")
        self.team = Team.objects.create(name="Team A")
        self.team.members.add(self.worker)
        self.team.project.add(self.project)

    def get_permission(self, codename):
        permission = Permission.objects.get(codename=codename)
        self.user.user_permissions.add(permission)
        self.client.login(username="testuser", password="password")

    def post_create_update_form(self, url_name, form_data, kwargs=None):
        url = reverse(url_name, kwargs=kwargs)
        response = self.client.post(url, data=form_data)
        return response

    def assert_redirects_and_exists(self, response, model, name):
        self.assertEqual(response.status_code, 302)
        self.assertTrue(model.objects.filter(name=name).exists())


class IndexViewTest(BaseTestCase):
    def test_index_view(self):
        response = self.client.get(reverse("manager:index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "manager/index.html")
        self.assertIn("worker", response.context)
        self.assertIn("projects", response.context)


class TaskListViewTest(BaseTestCase):
    def test_task_list_view(self):
        response = self.client.get(reverse("manager:task-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "manager/task_list.html")
        self.assertIn("search_form", response.context)
        self.assertContains(response, self.task.name)


class TaskDetailViewTest(BaseTestCase):
    def test_task_detail_view(self):
        response = self.client.get(reverse(
            "manager:task-detail",
            kwargs={"pk": self.task.pk}
        ))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "manager/task_detail.html")
        self.assertIn("can_complete", response.context)
        self.assertContains(response, self.task.name)


class TaskCompleteViewTest(BaseTestCase):
    def test_task_complete_view(self):
        self.task.assigned.add(self.worker)
        self.client.login(username="worker", password="password")
        response = self.client.post(reverse(
            "manager:task-complete",
            kwargs={"pk": self.task.pk}
        ))
        self.assertEqual(response.status_code, 302)
        self.task.refresh_from_db()
        self.assertTrue(self.task.is_completed)


class TaskDeleteViewTest(BaseTestCase):
    def test_task_delete_view(self):
        self.get_permission("view_task")
        response = self.client.get(reverse(
            "manager:task-delete",
            kwargs={"pk": self.task.pk}
        ))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(reverse(
            "manager:task-delete",
            kwargs={"pk": self.task.pk}
        ))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Task.objects.filter(pk=self.task.pk).exists())


class WorkerListViewTest(BaseTestCase):
    def test_worker_list_view(self):
        response = self.client.get(reverse("manager:worker-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "manager/worker_list.html")
        self.assertIn("search_form", response.context)
        self.assertContains(response, self.worker.username)


class WorkerDetailViewTest(BaseTestCase):
    def test_worker_detail_view(self):
        response = self.client.get(reverse(
            "manager:worker-detail",
            kwargs={"pk": self.worker.pk}
        ))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "manager/worker_detail.html")
        self.assertContains(response, self.worker.username)


class WorkerDeleteViewTest(BaseTestCase):
    def test_worker_delete_view(self):
        self.get_permission("view_worker")
        response = self.client.get(reverse(
            "manager:worker-delete",
            kwargs={"pk": self.worker.pk}
        ))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(reverse(
            "manager:worker-delete",
            kwargs={"pk": self.worker.pk}
        ))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Worker.objects.filter(pk=self.worker.pk).exists())


class WorkerUpdateViewTest(BaseTestCase):
    def test_worker_update_view(self):
        self.get_permission("view_worker")
        response = self.client.get(reverse(
            "manager:worker-update",
            kwargs={"pk": self.worker.pk}
        ))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "manager/worker_form.html")
        form_data = {
            "username": "updatedworker",
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "position": self.position.id,
        }
        response = self.post_create_update_form(
            "manager:worker-update",
            form_data,
            {"pk": self.worker.pk}
        )
        self.assertEqual(response.status_code, 302)
        self.worker.refresh_from_db()
        self.assertEqual(self.worker.username, "updatedworker")


class TeamListViewTest(BaseTestCase):
    def test_team_list_view(self):
        response = self.client.get(reverse("manager:team-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "manager/team_list.html")
        self.assertIn("search_form", response.context)
        self.assertContains(response, self.team.name)


class TeamDetailViewTest(BaseTestCase):
    def test_team_detail_view(self):
        response = self.client.get(reverse(
            "manager:team-detail",
            kwargs={"pk": self.team.pk}
        ))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "manager/team_detail.html")
        self.assertContains(response, self.team.name)


class TeamCreateViewTest(BaseTestCase):
    def test_team_create_view(self):
        self.get_permission("view_team")
        response = self.client.get(reverse("manager:team-create"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "manager/team_form.html")
        form_data = {
            "name": "New Team",
            "members": [self.worker.id],
            "project": [self.project.id],
        }
        response = self.post_create_update_form(
            "manager:team-create",
            form_data
        )
        self.assert_redirects_and_exists(response, Team, "New Team")


class TeamDeleteViewTest(BaseTestCase):
    def test_team_delete_view(self):
        self.get_permission("view_team")
        response = self.client.get(reverse(
            "manager:team-delete",
            kwargs={"pk": self.team.pk}
        ))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(reverse(
            "manager:team-delete",
            kwargs={"pk": self.team.pk}
        ))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Team.objects.filter(pk=self.team.pk).exists())


class TeamUpdateViewTest(BaseTestCase):
    def test_team_update_view(self):
        self.get_permission("view_team")
        response = self.client.get(reverse(
            "manager:team-update",
            kwargs={"pk": self.team.pk}
        ))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "manager/team_form.html")
        form_data = {
            "name": "Updated Team",
            "members": [self.worker.id],
            "project": [self.project.id],
        }
        response = self.post_create_update_form(
            "manager:team-update",
            form_data,
            {"pk": self.team.pk}
        )
        self.assertEqual(response.status_code, 302)
        self.team.refresh_from_db()
        self.assertEqual(self.team.name, "Updated Team")


class TagListViewTest(BaseTestCase):
    def test_tag_list_view(self):
        self.get_permission("view_tag")
        response = self.client.get(reverse("manager:tag-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "manager/tag_list.html")
        self.assertContains(response, self.tag.name)


class TagCreateViewTest(BaseTestCase):
    def test_tag_create_view(self):
        self.get_permission("view_tag")
        response = self.client.get(reverse("manager:tag-create"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "manager/tag_form.html")
        form_data = {
            "name": "New Tag",
        }
        response = self.post_create_update_form(
            "manager:tag-create",
            form_data
        )
        self.assert_redirects_and_exists(response, Tag, "New Tag")


class TagDeleteViewTest(BaseTestCase):
    def test_tag_delete_view(self):
        self.get_permission("view_tag")
        response = self.client.get(reverse(
            "manager:tag-delete",
            kwargs={"pk": self.tag.pk}
        ))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(reverse(
            "manager:tag-delete",
            kwargs={"pk": self.tag.pk}
        ))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Tag.objects.filter(pk=self.tag.pk).exists())


class TagUpdateViewTest(BaseTestCase):
    def test_tag_update_view(self):
        self.get_permission("view_tag")
        response = self.client.get(reverse(
            "manager:tag-update",
            kwargs={"pk": self.tag.pk}
        ))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "manager/tag_form.html")
        form_data = {
            "name": "Updated Tag",
        }
        response = self.post_create_update_form(
            "manager:tag-update",
            form_data,
            {"pk": self.tag.pk}
        )
        self.assertEqual(response.status_code, 302)
        self.tag.refresh_from_db()
        self.assertEqual(self.tag.name, "Updated Tag")


class PositionListViewTest(BaseTestCase):
    def test_position_list_view(self):
        self.get_permission("view_position")
        response = self.client.get(reverse("manager:position-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "manager/position_list.html")
        self.assertContains(response, self.position.name)


class PositionCreateViewTest(BaseTestCase):
    def test_position_create_view(self):
        self.get_permission("view_position")
        response = self.client.get(reverse("manager:position-create"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "manager/position_form.html")
        form_data = {
            "name": "New Position",
        }
        response = self.post_create_update_form(
            "manager:position-create",
            form_data
        )
        self.assert_redirects_and_exists(response, Position, "New Position")


class PositionDeleteViewTest(BaseTestCase):
    def test_position_delete_view(self):
        self.get_permission("view_position")
        response = self.client.get(reverse(
            "manager:position-delete",
            kwargs={"pk": self.position.pk}
        ))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(reverse(
            "manager:position-delete",
            kwargs={"pk": self.position.pk}
        ))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Position.objects.filter(pk=self.position.pk).exists())


class PositionUpdateViewTest(BaseTestCase):
    def test_position_update_view(self):
        self.get_permission("view_position")
        response = self.client.get(reverse(
            "manager:position-update",
            kwargs={"pk": self.position.pk}
        ))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "manager/position_form.html")
        form_data = {
            "name": "Updated Position",
        }
        response = self.post_create_update_form(
            "manager:position-update",
            form_data,
            {"pk": self.position.pk}
        )
        self.assertEqual(response.status_code, 302)
        self.position.refresh_from_db()
        self.assertEqual(self.position.name, "Updated Position")
