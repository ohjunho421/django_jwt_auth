# auth_app/utils.py
from rest_framework.views import exception_handler
from rest_framework.exceptions import ValidationError, AuthenticationFailed, NotAuthenticated
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework.response import Response
from rest_framework import status

def custom_exception_handler(exc, context):
    """
    커스텀 예외 처리기
    """
    response = exception_handler(exc, context)
    
    if isinstance(exc, ValidationError):
        # 사용자 이름 중복 오류 처리
        if 'username' in exc.detail and '이미 가입된 사용자입니다.' in str(exc.detail['username']):
            return Response({
                'error': {
                    'code': 'USER_ALREADY_EXISTS',
                    'message': '이미 가입된 사용자입니다.'
                }
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # 로그인 실패 처리
        if '아이디 또는 비밀번호가 올바르지 않습니다.' in str(exc.detail):
            return Response({
                'error': {
                    'code': 'INVALID_CREDENTIALS',
                    'message': '아이디 또는 비밀번호가 올바르지 않습니다.'
                }
            }, status=status.HTTP_401_UNAUTHORIZED)
    
    # 인증 오류 처리
    if isinstance(exc, NotAuthenticated):
        return Response({
            'error': {
                'code': 'TOKEN_NOT_FOUND',
                'message': '토큰이 없습니다.'
            }
        }, status=status.HTTP_401_UNAUTHORIZED)
    
    # 토큰 유효성 오류 처리
    if isinstance(exc, (InvalidToken, TokenError)):
        if 'Token is invalid or expired' in str(exc):
            return Response({
                'error': {
                    'code': 'TOKEN_EXPIRED',
                    'message': '토큰이 만료되었습니다.'
                }
            }, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({
                'error': {
                    'code': 'INVALID_TOKEN',
                    'message': '토큰이 유효하지 않습니다.'
                }
            }, status=status.HTTP_401_UNAUTHORIZED)
    
    # 기본 예외 처리
    if response is not None:
        return response
    
    # 처리되지 않은 예외
    return Response({
        'error': {
            'code': 'SERVER_ERROR',
            'message': '서버 오류가 발생했습니다.'
        }
    }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)