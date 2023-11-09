from django.db import models
from django.contrib.auth.models import User
from cafe.models import Cafe


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cafe = models.ForeignKey(Cafe, on_delete=models.CASCADE)
    is_cafe_admin = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
