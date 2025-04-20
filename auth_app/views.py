# auth_app/views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .serializers import SignupSerializer, LoginSerializer, UserSerializer

class SignupView(APIView):
    """
    회원가입 API
    """
    @swagger_auto_schema(
        request_body=SignupSerializer,
        responses={
            201: openapi.Response('회원가입 성공', UserSerializer),
            400: openapi.Response('회원가입 실패', 
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'error': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'code': openapi.Schema(type=openapi.TYPE_STRING, description='에러 코드'),
                                'message': openapi.Schema(type=openapi.TYPE_STRING, description='에러 메시지')
                            }
                        )
                    }
                )
            )
        }
    )
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # 사용자 정보 반환
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)

class LoginView(APIView):
    """
    로그인 API
    """
    @swagger_auto_schema(
        request_body=LoginSerializer,
        responses={
            200: openapi.Response('로그인 성공', 
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'token': openapi.Schema(type=openapi.TYPE_STRING, description='JWT 토큰')
                    }
                )
            ),
            401: openapi.Response('로그인 실패', 
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'error': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'code': openapi.Schema(type=openapi.TYPE_STRING, description='에러 코드'),
                                'message': openapi.Schema(type=openapi.TYPE_STRING, description='에러 메시지')
                            }
                        )
                    }
                )
            )
        }
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        
        # JWT 토큰 생성
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'token': str(refresh.access_token)
        }, status=status.HTTP_200_OK)

class UserView(APIView):
    """
    사용자 정보 조회 API
    (인증 테스트용)
    """
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        responses={
            200: UserSerializer,
            401: openapi.Response('인증 실패', 
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'error': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'code': openapi.Schema(type=openapi.TYPE_STRING, description='에러 코드'),
                                'message': openapi.Schema(type=openapi.TYPE_STRING, description='에러 메시지')
                            }
                        )
                    }
                )
            )
        }
    )
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)