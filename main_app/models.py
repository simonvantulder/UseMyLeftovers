from django.db import models
from datetime import datetime
import bcrypt 
import re # import regex for email validation

class UserManager(models.Manager):
    def login_validator(self, post_data):
        errors = {}

        user_list = User.objects.filter(email = post_data['email'])
        if len(user_list) > 0:
            user = user_list[0]
            if not bcrypt.checkpw(post_data['password'].encode(), user.password.encode()):
                errors['password'] = "INVALID CREDENTIALS"
        else:
                errors['email'] = "INVALID CREDENTIALS"
        return errors


    def validator(self, post_data):
        errors = {}

        #all errors are strings
        if len(post_data['first_name']) < 2:
            errors['first_name'] = "First name must be longer than 1 character"
        if len(post_data['last_name']) < 2:
            errors['last_name'] = "Last name must be longer than 1 character"

        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

        if not EMAIL_REGEX.match(post_data['email']):
            errors['email'] = "Invalid Email address!"
        else:
            user_list = User.objects.filter(email = post_data['email'])
            if len(user_list) > 0:
                errors['email'] = 'Email is being used by another user.'
        if len(post_data['password']) < 3:
            errors['password'] = "Passwords must be at least 4 characters long."
        elif post_data['password'] != post_data['confirm_pw']:
            errors['confirm_pw'] = "Password and Confirm Password must match."

        return errors



class User(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    objects = UserManager()

    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):        
        return f"< {self.first_name} ({self.id})>"


class Category(models.Model):
    name = models.CharField(max_length=100)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)


class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    quantity = models.IntegerField()
    # null = true, example 10 apples are their own unit
    unit = models.CharField(max_length=25, null = True)

    # allow expiration to be optional 
    # ie some dry good have Very long shelf lives, impractical to put in
    expiration = models.DateField(null = True) 
    # organize ingredients by category
    category = models.ForeignKey("Category", related_name = "ingredients", on_delete = models.CASCADE)
    # assign ingredients to a user's pantry
    chef = models.ForeignKey("User", related_name = "ingredients", null = True, on_delete = models.CASCADE)

    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

