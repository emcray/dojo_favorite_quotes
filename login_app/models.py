from django.db import models
import re
import bcrypt

class UserManager(models.Manager):
    def reg_validate(self, postData):
        errors = {}
        check = User.objects.filter(email = postData['email'])
        if len(postData['first_name']) < 2:
            errors['first_name'] = "First name must be at least 2 characters long"
        if len(postData['last_name']) < 2:
            errors['last_name'] = "Last name must be at least 2 characters long"

        if len(postData['password']) < 8:
            errors['password'] = "Password must be at least 8 characters long"
        elif postData['password'] != postData['confirm_pass']:
            errors['password'] = "Passwords do not match"

        EMAIL_REGEX = re.compile('^[_a-z0-9-]+(.[_a-z0-9-]+)@[a-z0-9-]+(.[a-z0-9-]+)(.[a-z]{2,4})$')
        if len(postData['email']) < 1:
            errors['email'] = "Email cannont be left blank"
        elif not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Please enter a valide email address"
        elif check:
            errors['email'] = "Email is already in use"
        
        return errors

    def login_validate(self, postData):
        errors = {}
        check_user = User.objects.filter(email = postData['email'])
        if not check_user: 
            errors['email'] = "Email has not been registered."
        else:
            if not bcrypt.checkpw(postData['password'].encode(), check_user[0].password.encode()):
                errors['email'] = "Email and password do not match!"
        return errors

    def update_validate(self, postData):
        errors = {}
        check = User.objects.filter(email = postData['email'])
        if len(postData['first_name']) < 2:
            errors['first_name'] = "First name must be at least 2 characters long"
        if len(postData['last_name']) < 2:
            errors['last_name'] = "Last name must be at least 2 characters long"

        EMAIL_REGEX = re.compile('^[_a-z0-9-]+(.[_a-z0-9-]+)@[a-z0-9-]+(.[a-z0-9-]+)(.[a-z]{2,4})$')
        if len(postData['email']) < 1:
            errors['email'] = "Email cannont be left blank"
        elif not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Please enter a valide email address"
        elif check:
            errors['email'] = "Email is already in use"
        
        return errors


class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.EmailField(max_length=45)
    password = models.CharField(max_length=45)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    objects = UserManager()


