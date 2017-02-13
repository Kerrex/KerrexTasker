from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
import json

# Create your tests here.
from taskbackend.models import Project, ProjectRole, UserProjectRole
from taskbackend.views import ProjectsView


class ProjectsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('test', password='test')
        self.user_token = Token.objects.get(user=self.user)
        self.user2 = User.objects.create_user('test2', password='test2')
        self.user2_token = Token.objects.get(user=self.user2)
        self.project = Project.objects.create(name='without_users', description='test', is_active=True, owner=self.user)
        self.project2 = Project.objects.create(name='with_users', description='test', is_active=True, owner=self.user)
        self.projectrole = ProjectRole.objects.create(can_edit=True, can_create_board=True, project=self.project)
        self.userprojectrole = UserProjectRole.objects.create(user=self.user2, project_role=self.projectrole)

    # test as owner
    def test_get(self):
        client = APIClient()
        client.force_authenticate(user=self.user)
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_token.key)
        response = client.get('/api/projects')

        json_str = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response.status_code, 200, 'HTTP 200OK expected')
        self.assertEqual(self.project.name, json_str['results'][0]['name'], 'Expected project name')
        self.assertEqual(self.project.owner.id, json_str['results'][0]['owner'], 'Expected owner id')
