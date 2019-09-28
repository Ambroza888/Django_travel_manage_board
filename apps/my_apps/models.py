from django.db import models
import re

class UserManager(models.Manager):
  def basic_validator(self, postData):
    errors = {}
    if len(postData['name']) < 2:
      errors['name'] = "The name needs to be more than 2 characters BRAAA"
    if len(postData['alias']) < 2:
      errors['alias'] = "Choose better nickname BRa"
    if postData['password'] != postData['re_password']:
      errors['password'] = "Your password is not matching put some glasses"
    if len(postData['password']) < 5:
      errors['password'] = "Your password need to be more than 5 characters"
    EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
    if not EMAIL_REGEX.match(postData['email']):
      errors['email'] = "Your email address is not in the right order don't cheat on my front end please !"
    return errors

  def basic_validator_trip(self, postData):
    errors = {}
    if len(postData['destination']) < 3:
      errors['destination'] = "Come on Navia,you know needs to be more than 3 characters ..."
    if len(postData['plan']) == 0:
      errors['plan'] = "Naviaaa, we need a plan please !!!"
    if len(postData['start_date']) < 5:
      errors['start_date'] = "Stan you are Torchering me !!!"
    if len(postData['end_date']) < 5:
      errors['start_date'] = "Stan you are Torchering me !!!"
    return errors
  def basic_validator_edit_trip(self,postData):
    errors = {}
    if len(postData['start_date']) < 5:
      errors['start_date'] = "Stan you are Torchering me !!!"
    if len(postData['end_date']) < 5:
      errors['start_date'] = "Stan you are Torchering me !!!"
    return errors

  



class User(models.Model):
  name = models.CharField(max_length=255)
  alias = models.CharField(max_length=255)
  email = models.CharField(max_length=255)
  password = models.CharField(max_length=255)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  objects = UserManager()

class Trip(models.Model):
  destination = models.CharField(max_length=255)
  start_date = models.DateTimeField()
  end_date = models.DateTimeField()
  plan = models.TextField()
  user = models.ForeignKey(User, related_name="trips")
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  objects = UserManager()