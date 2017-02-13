from django.conf import settings
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class Project(models.Model):
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=50, blank=False, null=False)
    description = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True, null=False)


class Board(models.Model):
    manager_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    project = models.ForeignKey(Project, null=False, on_delete=models.CASCADE)


class Category(models.Model):
    name = models.CharField(max_length=20, unique=True)
    order = models.IntegerField(unique=True, null=False)
    board = models.ForeignKey(Board, null=False, on_delete=models.CASCADE)


class Tile(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    creator = models.ForeignKey(User, related_name='creator')
    assigned_user = models.ForeignKey(User, related_name='assigned_user')
    PRIORITY_CHOICES = (
        ('L', 'Low'),
        ('M', 'Medium'),
        ('H', 'High'),
        ('C', 'Critical')
    )
    priority = models.CharField(max_length=1, choices=PRIORITY_CHOICES)
    is_active = models.BooleanField(default=True)
    category = models.ForeignKey(Category, null=False, on_delete=models.CASCADE)
    order = models.IntegerField(unique=True, null=False)


class Comment(models.Model):
    user = models.ForeignKey(User, null=False)
    date = models.DateTimeField(auto_now=True, null=False)
    content = models.TextField()
    tile = models.ForeignKey(Tile, on_delete=models.CASCADE)


class ProjectRole(models.Model):
    can_edit = models.BooleanField(null=False)
    can_create_board = models.BooleanField(null=False)
    project = models.ForeignKey(Project, null=False, on_delete=models.CASCADE)


class BoardRole(models.Model):
    can_edit = models.BooleanField(null=False)
    can_create_tile = models.BooleanField(null=False)
    board = models.ForeignKey(Board, null=False, on_delete=models.CASCADE)


class UserProjectRole(models.Model):
    user = models.ForeignKey(User, null=False)
    project_role = models.ForeignKey(ProjectRole, null=False)
    date_add = models.DateTimeField(null=False, auto_now=True)


class UserBoardRole(models.Model):
    user = models.ForeignKey(User, null=False)
    board_role = models.ForeignKey(BoardRole, null=False)
    date_add = models.DateTimeField(null=False, auto_now=True)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
