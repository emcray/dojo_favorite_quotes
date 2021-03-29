from django.db import models
from datetime import datetime
from login_app.models import User, UserManager
from django.db.models import Count, Sum

class AuthorManager(models.Manager):
    def author_validate(self, postData):
        errors = {}

        if len(postData['author_name']) < 3:
            errors['author_name'] = "Author Name must be at least 3 characters long."

        return errors

class Author(models.Model):
    name = models.CharField(max_length=45)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = AuthorManager()

class QuoteManager(models.Manager):
    def quote_validate(self, postData):
        errors = {}

        if len(postData['quote']) < 10:
            errors['quote'] = "Quote must be at least 10 characters long."

        return errors

class Quote(models.Model):
    content = models.TextField(max_length=255)
    author = models.ForeignKey(Author, related_name = "author", on_delete=models.CASCADE)
    posted_by = models.ForeignKey(User, related_name = "user", on_delete=models.CASCADE)
    liked_by = models.ManyToManyField(User, related_name="likes")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = QuoteManager()

