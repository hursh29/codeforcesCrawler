from django.db import models

class all_users(models.Model):
    rank      = models.CharField(max_length=60,default='great')
    rankCount = models.IntegerField()
 
class all_usersRating(models.Model):
    rating      = models.IntegerField()
    ratingCount = models.IntegerField()

class Educational(models.Model):
    contestId    = models.IntegerField()
    contestName  = models.CharField(max_length=100,default='----')
    problemList  = models.CharField(max_length=100,default='A ')

class Div_1(models.Model):
    contestId = models.IntegerField()
    contestName  = models.CharField(max_length=100,default='----')
    problemList  = models.CharField(max_length=100,default='A ')
    
class Div_2(models.Model):
    contestId = models.IntegerField()
    contestName  = models.CharField(max_length=100,default='----')
    problemList  = models.CharField(max_length=100,default='A ')
    
class Div_3(models.Model):
    contestId = models.IntegerField()
    contestName  = models.CharField(max_length=100,default='----')
    problemList  = models.CharField(max_length=100,default='A ')
    
class Global(models.Model):
    contestId = models.IntegerField()
    contestName  = models.CharField(max_length=100,default='----')
    problemList  = models.CharField(max_length=100,default='A ')
    
class Others(models.Model):
    contestId = models.IntegerField()
    contestName  = models.CharField(max_length=100,default='----')
    problemList  = models.CharField(max_length=100,default='A ')

# Create your models here.
