# Django JWT Authentication API

이 프로젝트는 JWT(JSON Web Token)를 사용한 인증 시스템을 구현한 Django 기반 RESTful API입니다.

## 기능

- 회원가입 (Signup)
- 로그인 (Login)
- 사용자 정보 조회 (인증 테스트용)

## API 엔드포인트

| 경로 | 메소드 | 설명 | 인증 필요 |
|------|--------|------|-----------|
| `/signup` | POST | 새 사용자 등록 | 아니오 |
| `/login` | POST | 사용자 로그인 및 JWT 토큰 발급 | 아니오 |
| `/user` | GET | 현재 인증된 사용자 정보 조회 | 예 |

## Swagger UI를 통한 API 문서 및 테스트

Swagger UI를 사용하여 API를 문서화하고 테스트할 수 있습니다.

### Swagger UI 접속 방법

```
http://18.143.75.190/swagger/
```

Swagger UI를 통해 다음 작업을 수행할 수 있습니다:
- 모든 API 엔드포인트 목록 확인
- API 요청에 필요한 파라미터 확인
- "Try it out" 기능을 통한 API 직접 테스트
- 응답 형식 및 상태 코드 확인

### API 테스트 단계

1. Swagger UI 페이지 접속
2. 테스트할 API 엔드포인트 선택 (예: /signup, /login, /user)
3. "Try it out" 버튼 클릭
4. 필요한 파라미터 입력
5. "Execute" 버튼 클릭
6. 응답 확인

인증이 필요한 API를 테스트할 경우 (/user):
1. 먼저 /login API를 통해 토큰 발급
2. 발급받은 토큰을 "Authorize" 버튼을 클릭하여 입력
3. "Bearer" 인증 방식 선택 후 토큰 값 입력 (예: Bearer eyJhbGciOiJIUzI1NiIs...)
4. "Authorize" 버튼 클릭
5. 이제 인증이 필요한 API를 테스트할 수 있습니다

## API 테스트 방법 (기타)

### 1. cURL을 사용한 API 테스트

#### 회원가입 (Signup)

```bash
curl -X POST http://18.143.75.190/signup \
  -H "Content-Type: application/json" \
  -d '{"username":"테스트유저", "password":"테스트비밀번호", "nickname":"테스트닉네임"}'
```

예상 응답:
```json
{
  "username": "테스트유저",
  "nickname": "테스트닉네임"
}
```

#### 로그인 (Login)

```bash
curl -X POST http://18.143.75.190/login \
  -H "Content-Type: application/json" \
  -d '{"username":"테스트유저", "password":"테스트비밀번호"}'
```

예상 응답:
```json
{
  "token": "eyJhbGciOiJIUzI1NiIs..."
}
```

#### 사용자 정보 조회 (인증 필요)

```bash
curl -X GET http://18.143.75.190/user \
  -H "Authorization: Bearer 여기에_토큰_입력"
```

예상 응답:
```json
{
  "username": "테스트유저",
  "nickname": "테스트닉네임"
}
```

### 2. Postman을 사용한 API 테스트

1. Postman 애플리케이션을 다운로드하고 실행합니다.
2. 새 요청을 생성합니다.
3. 요청 URL과 메소드를 설정합니다.
4. 'Headers' 탭에서 Content-Type을 'application/json'으로 설정합니다.
5. 'Body' 탭에서 'raw'를 선택하고 JSON 형식으로 데이터를 입력합니다.
6. 인증이 필요한 요청의 경우, 'Headers' 탭에서 Authorization을 'Bearer 여기에_토큰_입력'으로 설정합니다.
7. 'Send' 버튼을 클릭하여 요청을 보냅니다.

### 3. Python Requests 라이브러리를 사용한 API 테스트

```python
import requests
import json

# API 주소
base_url = "http://18.143.75.190"

# 회원가입
signup_data = {
    "username": "테스트유저",
    "password": "테스트비밀번호",
    "nickname": "테스트닉네임"
}
signup_response = requests.post(f"{base_url}/signup", json=signup_data)
print("회원가입 응답:", signup_response.status_code, signup_response.json())

# 로그인
login_data = {
    "username": "테스트유저",
    "password": "테스트비밀번호"
}
login_response = requests.post(f"{base_url}/login", json=login_data)
print("로그인 응답:", login_response.status_code, login_response.json())

# 토큰 추출
token = login_response.json().get('token')

# 사용자 정보 조회 (인증 필요)
headers = {"Authorization": f"Bearer {token}"}
user_response = requests.get(f"{base_url}/user", headers=headers)
print("사용자 정보 응답:", user_response.status_code, user_response.json())
```

## API 응답 형식

### 성공 응답

API 요청이 성공하면 적절한 HTTP 상태 코드(2xx)와 함께 응답 데이터가 반환됩니다.

### 오류 응답

API 요청이 실패하면 적절한 HTTP 상태 코드(4xx 또는 5xx)와 함께 다음과 같은 형식의 오류 메시지가 반환됩니다:

```json
{
  "error": {
    "code": "오류_코드",
    "message": "오류 메시지"
  }
}
```

#### 주요 오류 코드

| 코드 | 설명 |
|------|------|
| `USER_ALREADY_EXISTS` | 이미 가입된 사용자입니다. |
| `INVALID_CREDENTIALS` | 아이디 또는 비밀번호가 올바르지 않습니다. |
| `TOKEN_NOT_FOUND` | 토큰이 없습니다. |
| `INVALID_TOKEN` | 토큰이 유효하지 않습니다. |
| `TOKEN_EXPIRED` | 토큰이 만료되었습니다. |
| `SERVER_ERROR` | 서버 오류가 발생했습니다. |

## 보안 고려사항

- 프로덕션 환경에서는 HTTPS를 사용하여 API 통신을 암호화하는 것이 좋습니다.
- JWT 토큰은 보안에 민감한 정보이므로 안전하게 저장하고 관리해야 합니다.
- 토큰에는 만료 시간이 설정되어 있으며, 만료된 토큰은 더 이상 유효하지 않습니다.