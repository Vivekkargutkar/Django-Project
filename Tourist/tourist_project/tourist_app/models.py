from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class contact(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    subject = models.CharField(max_length=50)
    msg = models.CharField(max_length=300)


class places(models.Model):
    pname = models.CharField(max_length=50)
    days = models.IntegerField()
    person = models.IntegerField()
    price = models.IntegerField()
    description = models.CharField(max_length=300)
    pimage = models.ImageField(upload_to='image')

    def __str__(self):
        return self.pname


class booking(models.Model):
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    contact = models.IntegerField()
    date = models.DateField()
    address = models.CharField(max_length=300 ,null=True, blank=True)
    msg = models.CharField(max_length=300)
    uid = models.ForeignKey(User,on_delete=models.CASCADE,db_column="uid",null=True)
    pid = models.ForeignKey(places,on_delete=models.CASCADE,db_column="pid",null=True)

    file = models.FileField(upload_to='media2/', null=True, blank=True)

    def __str__(self):
        return self.name