from rest_framework import serializers
from .models import CustomUser

class CustomUserSerializers(serializers.ModelSerializer):
    # confirmed_password = serializers.CharField(max_length=128, write_only=True)
    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name','email', 'password')
        read_only_fields = ('id' , 'date_joined')
        
        
class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('username', 'password', 'email')
        
        