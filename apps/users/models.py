from django.db import models

import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
import bcrypt


class UserManager(models.Manager):
  def validate(self, form):
    errors = []
    #name validations
    if len(form['first_name']) < 2:
      errors.append("Invalid First Name!")
    if not form['first_name'].isalpha:
      errors.append("Invalid First Name!")
    if len(form['last_name']) < 2:
      errors.append("Invalid Last Name!")
    if not form['last_name'].isalpha:
      errors.append("Invalid Last Name!")
    #email validations
    if not EMAIL_REGEX.match(form['email']):
      errors.append('Invalid Email Address!')
    try:
      self.get(email=form['email'])
      errors.append("Email already in use!")
    except:
      pass
    #username validations
    try:
      self.get(username=form['username'])
      errors.append("Username already in use!")
    except:
      pass
    #password validations
    if len(form['password']) < 8:
      errors.append("Password must be at least 8 characters!")
    if form['password'] != form['confirm']:
      errors.append("Password DO NOT match!")
    return errors

  def create_user(self, user_data):
    import datetime
    pw_hash = bcrypt.hashpw(user_data['password'].encode(), bcrypt.gensalt())
    user = self.create(
      first_name = user_data['first_name'],
      last_name = user_data['last_name'],
      username = user_data['username'],
      email = user_data['email'],
      password = pw_hash,
      created_at = datetime.datetime.now(),
      updated_at = datetime.datetime.now()
    )
    return user

  def login(self, form):
    errors = []
    try:
      user = self.get(email=form['email'])
      if bcrypt.checkpw(form['password'].encode(),user.password.encode()):
        return(True,user.id)
      else:
        errors.append("Password incorrect!")
        return (False,errors)
    except:
      errors.append("Email does not exist!")
      return(False,errors)

class User(models.Model):
  first_name = models.CharField(max_length=255)
  last_name = models.CharField(max_length=255)
  username = models.CharField(max_length=255)
  email = models.CharField(max_length=255)
  password = models.CharField(max_length=255)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  objects = UserManager()

