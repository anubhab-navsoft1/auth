from .models import CustomUser
from django.contrib.auth.backends import BaseBackend

class CustomEmailBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        if username is None or password is None:
            return None

        try:
            user = CustomUser.objects.get(username=username)
            print("-----------auth", user)
        except CustomUser.DoesNotExist:
            return None

        if user.check_password(password):
            print("-----------", password)
            return user
        return None