from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authtoken.models import Token

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField(max_length=128, min_length=6)
    default_error_messages = {
        'invalid': 'Wrong Credentials'
    }

    class Meta:
        model = User
        fields = ('email', 'password')

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField(max_length=128, min_length=6)

    def validate(self, attrs):
        email = attrs.get('email','')
        password = attrs.get('password','')
        filtered_user_by_email = User.objects.filter(email=email)
        user = authenticate(email=email, password=password)
 
        if not user:
            raise AuthenticationFailed('Invalid credentials, try again')
        if not user.is_active:
            raise AuthenticationFailed('Account disabled, contact admin')
        token = Token.objects.get_or_create(user=user)

        return {
            'email': user.email,
            'token': token
        }

        return super().validate(attrs)
    class Meta:
        model = User
        fields = ['email', 'password']

class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    default_error_messages = {
        'bad_token': ('Token is invalid')
    }

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs
    
    def save(self, **kwargs):
        try: 
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('bad_token')
            