from django import forms
from django.db import models
from django.contrib.auth.models import AbstractUser

"""
User table with nick
Args: AbstractUser: username,first_name,last_name,email,password,groups,user_permissions,is_staff,is_active,is_superuser,last_login,date_joined
"""
class User(AbstractUser):
        nick = models.CharField(max_length=20)
        email = models.EmailField(unique=True)
        public_key1 = models.TextField(null=True)
        public_key2 = models.TextField(null=True)

class ReviewForm(forms.Form):
        image = forms.ImageField(label='image', max_length=100)
        

"""
Review Table with user,concert,content,photo,sit_sector,stars,up_votes,down_votes,date
Args: models.Model
"""
class Review(models.Model):
        user_id = models.ForeignKey('User', on_delete=models.CASCADE)
        concert = models.CharField(max_length=100)
        venue = models.ForeignKey('Location', on_delete=models.CASCADE, to_field='name')
        sit_sector = models.CharField(max_length=30)
        content = models.TextField(max_length=500)
        photo = models.ImageField(null=True, blank=True, upload_to='images/')
        stars = models.PositiveSmallIntegerField()
        votes = models.SmallIntegerField(default=0) #positive-negative votes
        total_votes = models.PositiveSmallIntegerField(default=0) #total number of votes
        date = models.DateTimeField()
        def __str__(self):
                return self.concert        

"""
Comment table with user,content,review,date 
Args: models.Model
"""
class Comment(models.Model):
        user_id = models.ForeignKey('User', on_delete=models.CASCADE)
        content = models.TextField()
        review_id = models.ForeignKey('Review', on_delete=models.CASCADE)
        date = models.DateTimeField()

"""
Location table with name,addres,city,country
Args: models.Model
"""
class Location(models.Model):
        name = models.CharField(max_length=100, unique=True)
        address = models.CharField(max_length=200, null=True, blank=True)
        city = models.CharField(max_length=100, null=True, blank=True)
        country = models.CharField(max_length=100, null=True, blank=True)
        def __str__(self):
                return self.name

"""
#Cote_Review table with user,review,is_positive
Args: models.Model
"""
class Vote_Review(models.Model):
        user = models.ForeignKey('User', on_delete=models.CASCADE)
        review = models.ForeignKey('Review', on_delete=models.CASCADE)
        is_positive = models.SmallIntegerField() #1=voted positive ; -1=voted negative ; 0=havent voted

"""
Nuevos Models para la firma
"""
class Document(models.Model):
    creator = models.ForeignKey('User', on_delete=models.CASCADE, related_name='creator')
    title = models.TextField()
    content = models.TextField()
    sign = models.TextField()
    request_to = models.ForeignKey('User', on_delete=models.CASCADE, related_name='request_to')
    accepted = models.IntegerField()
    file_txt = models.FileField(null=True, blank=True)
    def __str__(self):
        return self.title