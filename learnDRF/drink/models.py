from django.db import models
from django.contrib.auth.models import User

class Notebook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notebooks')
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Note(models.Model):
    notebook = models.ForeignKey(Notebook, related_name='notes', on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_trashed = models.BooleanField(default=False)

    def __str__(self):
        return self.title
