from django.db import models


class User(models.Model):

    gender = (
        ('male'),
        ('female'),
    )

    name = models.CharField(max_length=128, unique=True)
    password = models.CharField(max_length=256)
    email = models.EmailField(unique=True)
    # sex = models.CharField(max_length=32, choices=gender, default="male")
    c_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-c_time"]
        # verbose_name = "用户"
        # verbose_name_plural = "用户"
