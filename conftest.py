import pytest
from django.conf import settings
from rest_framework.test import APIClient

# Django 설정이 올바르게 로드되도록 설정
pytest_plugins = [
    'pytest_django',
]

@pytest.fixture
def api_client():
    """
    API 클라이언트 픽스처
    """
    return APIClient()