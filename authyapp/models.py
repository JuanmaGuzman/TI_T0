import json
from django.db import models



class User(models.Model):
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    age = models.IntegerField(default=0)
    psu_score = models.IntegerField(default=0)
    university = models.CharField(max_length=200)
    gpa_score = models.FloatField(default=0)
    job = models.CharField(max_length=200)
    salary = models.FloatField(default=0)
    promotion = models.BooleanField(default=0)
    hospital = models.CharField(max_length=200)
    operations = models.TextField()
    medical_debt = models.FloatField(default=0)

    def __str__(self):
        return self.username
    
    def set_operations(self, x):
        self.operations = json.dumps(x)

    def get_operations(self):
        return json.loads(self.operations)
    

class UserToken(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=200)

class AccessToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    app_id = models.CharField(max_length=200)
    scopes = models.CharField(max_length=200)
    expiration = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.scopes


class AccessTokenRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    app_id = models.CharField(max_length=200)
    nonce = models.CharField(max_length=200)
    expiration = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nonce
