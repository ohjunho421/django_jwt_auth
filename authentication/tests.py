import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from .models import User

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def create_user():
    user = User.objects.create_user(
        username="testuser",
        password="testpassword",
        nickname="TestNick"
    )
    return user

@pytest.mark.django_db
class TestSignupView:
    def test_login_nonexistent_user(self, api_client):
        """
        존재하지 않는 사용자로 로그인 실패 테스트
        """
        url = reverse('login')
        data = {
            'username': 'nonexistentuser',
            'password': 'testpassword'
        }
        
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == 401
        assert response.data['error']['code'] == 'INVALID_CREDENTIALS'
        assert response.data['error']['message'] == '아이디 또는 비밀번호가 올바르지 않습니다.'

@pytest.mark.django_db
class TestAuthenticationFlow:
    def test_authentication_required(self, api_client):
        """
        인증이 필요한 엔드포인트에 토큰 없이 접근할 때 실패 테스트
        """
        url = reverse('user')
        response = api_client.get(url)
        
        assert response.status_code == 401
        assert response.data['error']['code'] == 'TOKEN_NOT_FOUND'
        assert response.data['error']['message'] == '토큰이 없습니다.'
    
    def test_invalid_token(self, api_client):
        """
        유효하지 않은 토큰으로 인증 실패 테스트
        """
        url = reverse('user')
        api_client.credentials(HTTP_AUTHORIZATION='Bearer invalid_token')
        response = api_client.get(url)
        
        assert response.status_code == 401
        assert response.data['error']['code'] == 'INVALID_TOKEN'
        assert response.data['error']['message'] == '토큰이 유효하지 않습니다.'
    
    def test_successful_authentication(self, api_client):
        """
        회원가입, 로그인, 인증된 요청의 전체 흐름 테스트
        """
        # 1. 회원가입
        signup_url = reverse('signup')
        signup_data = {
            'username': 'flowuser',
            'password': 'password123',
            'nickname': 'FlowNick'
        }
        
        signup_response = api_client.post(signup_url, signup_data, format='json')
        assert signup_response.status_code == 201
        
        # 2. 로그인
        login_url = reverse('login')
        login_data = {
            'username': 'flowuser',
            'password': 'password123'
        }
        
        login_response = api_client.post(login_url, login_data, format='json')
        assert login_response.status_code == 200
        assert 'token' in login_response.data
        
        # 3. 인증이 필요한 엔드포인트 접근
        token = login_response.data['token']
        api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
        user_url = reverse('user')
        user_response = api_client.get(user_url)
        
        assert user_response.status_code == 200
        assert user_response.data['username'] == 'flowuser'
        assert user_response.data['nickname'] == 'FlowNick'_signup_success(self, api_client):
        """
        회원가입 성공 테스트
        """
        url = reverse('signup')
        data = {
            'username': 'newuser',
            'password': 'password123',
            'nickname': 'Nickname'
        }
        
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == 201
        assert response.data['username'] == 'newuser'
        assert response.data['nickname'] == 'Nickname'
        assert 'password' not in response.data
        
        # 사용자가 데이터베이스에 생성되었는지 확인
        assert User.objects.filter(username='newuser').exists()
    
    def test_signup_duplicate_username(self, api_client, create_user):
        """
        중복된 사용자 이름으로 회원가입 실패 테스트
        """
        url = reverse('signup')
        data = {
            'username': 'testuser',  # 이미 존재하는 사용자 이름
            'password': 'password123',
            'nickname': 'Nickname'
        }
        
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == 400
        assert response.data['error']['code'] == 'USER_ALREADY_EXISTS'
        assert response.data['error']['message'] == '이미 가입된 사용자입니다.'
    
    def test_signup_with_short_password(self, api_client):
        """
        짧은 비밀번호로 회원가입 실패 테스트
        """
        url = reverse('signup')
        data = {
            'username': 'newuser',
            'password': 'short',  # 8자 미만 비밀번호
            'nickname': 'Nickname'
        }
        
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == 400
        # 비밀번호 유효성 검사 오류 메시지 확인

@pytest.mark.django_db
class TestLoginView:
    def test_login_success(self, api_client, create_user):
        """
        로그인 성공 테스트
        """
        url = reverse('login')
        data = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == 200
        assert 'token' in response.data
        assert response.data['token'] is not None
    
    def test_login_invalid_credentials(self, api_client, create_user):
        """
        잘못된 자격 증명으로 로그인 실패 테스트
        """
        url = reverse('login')
        data = {
            'username': 'testuser',
            'password': 'wrongpassword'
        }
        
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == 401
        assert response.data['error']['code'] == 'INVALID_CREDENTIALS'
        assert response.data['error']['message'] == '아이디 또는 비밀번호가 올바르지 않습니다.'
    
    def test