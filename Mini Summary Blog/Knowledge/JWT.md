# Mã xác thực (JWT - JSON Web Token)
- [Hướng dẫn sử dụng JWT](https://200lab.io/blog/huong-dan-su-dung-jwt-trong-js/)
     Tóm tắt:
        I. Cấu tạo mã xác thực
            1. Header
            2. Payload
            3. Signature
        II. Chức năng mã xác thực
            1. 
            2. 
            3. 
            4. 
        III. Ví dụ về jwt
            1. Access Token
            2. Refresh Token
            3. Session Token
## I. Cấu tạo mã xác thực

### 1.Header

```JSON
{
  "alg": "HS256",
  "typ": "JWT"
}
```

- alg: thuật toán mã hoá 
- typ: Kiểu token (JWT)

### 2.Payload
![Payload jwt](https://statics.cdn.200lab.io/2024/06/payload-trong-jwt.jpg)

- Registered Claims:
    - iss (issuer): Người/hệ thống phát hành JWT.
    - sub (subject): Chủ thể của JWT, xác định rằng đây là người sở hữu hoặc có quyền truy cập resource (tài nguyên).
    - aud (audience): Người nhận mà JWT hướng tới.
    - exp (expiration time): Đậy là thời điểm JWT sẽ bị vô hiệu hóa.
    - nbf (not before time): JWT chỉ có hiệu lực sau thời gian này.
    - iat (issued at time): Thời gian JWT được tạo ra.
    - jti (JWT ID): Là mã duy nhất; có thể dùng để ngăn JWT bị tái sử dụng (cho phép một token chỉ được sử dụng một lần).

- Public Claims User Info:
    - name, given_name, family_name, middle_name: Thông tin tên nói chung của user
    - email : Email người dùng
    - locale : Địa chỉ của user.
    - profile, picture : URL thông tin người dùng

- Private Claims:
    - Tùy thuộc client và server quy định

### 3. Signature
- Cần Header + Payload + Secret key 
- Dùng base64UrlEncoded(header) + "." + base64UrlEncoded(payload) + "." + secretKey
- Dùng thuật toán các cryptography mật mã khoá (HS256(), HS384(), HS512(), RS256(), RS384(), RS512(), PS256(), PS384(), PS512(), EdDSA())

ví dụ dùng thuật toán HS256:
```JavaScript
header = {"alg": "HS256", "typ": "JWT"}
payload = {"sub": user_id, "name": username, "exp": expiration_time, "iat": datetime.datetime.utcnow()}
secretKey = "serectkey-1234"

HS256(base64UrlEncoded(header) + "." + base64UrlEncoded(payload) + "." + secretKey)
```
## II. Chức năng mã xác thực
## III. Ví dụ về jwt

```python
# jwt_helper.py

import jwt
import datetime
from typing import Dict, Any

# Cấu hình
SECRET_KEY = 'your-256-bit-secret'
ALGORITHM = 'HS256'
TOKEN_EXPIRATION_MINUTES = 30

def create_jwt(user_id: str) -> str:
    """
    Tạo JWT với user_id, tên user và thời gian hết hạn.

    :param  user_id: ID của người dùng,
            name: username

    :return: Mã JWT
    """

    expiration_time = datetime.datetime.utcnow() + datetime.timedelta(minutes=TOKEN_EXPIRATION_MINUTES)

    payload = {
        "sub": user_id,
        "name": username,
        "exp": expiration_time,
        "iat": datetime.datetime.utcnow()
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token

def decode_jwt(token: str) -> Dict[str, Any]:
    """
    Giải mã JWT để lấy thông tin payload.

    :param token: Mã JWT
    :return: Payload giải mã
    :raises: jwt.ExpiredSignatureError, jwt.InvalidTokenError
    """
    try:
        decoded_payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return decoded_payload
    except jwt.ExpiredSignatureError:
        raise jwt.ExpiredSignatureError("Token đã hết hạn.")
    except jwt.InvalidTokenError:
        raise jwt.InvalidTokenError("Token không hợp lệ.")
```

## 1. Access Token
## 2. Refresh Token
## 3. Session Token