from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Project(models.Model):
    owner_id = models.ForeignKey(User, on_delete=models.SET_NULL)
    name = models.CharField(max_length=50, blank=False, null=False)
    description = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True, null=False)


class Board(models.Model):
    manager_id = models.ForeignKey(User, on_delete=models.SET_NULL)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    project = models.ForeignKey(Project, null=False, on_delete=models.CASCADE)


class Category(models.Model):
    name = models.CharField(max_length=20, unique=True)
    board = models.ForeignKey(Board, null=False, on_delete=models.CASCADE)


class Tile(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    creator = models.ForeignKey(User)
    assigned_user = models.ForeignKey(User)
    PRIORITY_CHOICES = (
        ('L', 'Low'),
        ('M', 'Medium'),
        ('H', 'High'),
        ('C', 'Critical')
    )
    priority = models.CharField(max_length=1, choices=PRIORITY_CHOICES)
    is_active = models.BooleanField(default=True)
    category = models.ForeignKey(Category, null=False, on_delete=models.CASCADE)


class Comment(models.Model):
    user = models.ForeignKey(User, null=False)
    date = models.DateTimeField(auto_now=True, null=False)
    content = models.TextField()
    tile = models.ForeignKey(Tile, on_delete=models.CASCADE)


class ProjectRole(models.Model):
    can_edit = models.BooleanField(null=False)
    can_create_board = models.BooleanField(null=False)
    user = models.ManyToManyField(User)
    project = models.ForeignKey(Project, null=False, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('user', 'project'),)


class BoardRole(models.Model):
    can_edit = models.BooleanField(null=False)
    can_create_tile = models.BooleanField(null=False)
    board = models.ForeignKey(Board, null=False, on_delete=models.CASCADE)
    user = models.ManyToManyField(User)

    class Meta:
        unique_together = (('user', 'board'),)
