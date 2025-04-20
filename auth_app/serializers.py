# auth_app/serializers.py
from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate

class SignupSerializer(serializers.ModelSerializer):
    """
    회원가입을 위한 시리얼라이저
    """
    password = serializers.CharField(write_only=True, min_length=8)
    
    class Meta:
        model = User
        fields = ('username', 'password', 'nickname')
    
    def validate_username(self, value):
        """
        사용자 이름이 이미 존재하는지 확인
        """
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("이미 가입된 사용자입니다.")
        return value
    
    def create(self, validated_data):
        """
        사용자 생성
        """
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            nickname=validated_data['nickname']
        )
        return user

class LoginSerializer(serializers.Serializer):
    """
    로그인을 위한 시리얼라이저
    """
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, data):
        """
        사용자 인증
        """
        user = authenticate(username=data['username'], password=data['password'])
        if user is None:
            raise serializers.ValidationError("아이디 또는 비밀번호가 올바르지 않습니다.")
        
        return {
            'user': user
        }

class UserSerializer(serializers.ModelSerializer):
    """
    사용자 정보를 위한 시리얼라이저
    """
    class Meta:
        model = User
        fields = ('username', 'nickname')