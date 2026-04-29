## Day 2 - Create User Success Request

### Goal
Create the first executable Postman request for the STM API.

### Request
- Folder: User
- Name: Create user - success - 201
- Method: POST
- URL: `{{base_url}}/api/v1/users/`

### Request Body
```json
{
  "username": "postman_user_01",
  "email": "postman_user_01@example.com",
  "password": "123456"
}


---

# 明天 Day 3 建議任務

明天做：

**Login - valid credentials - 200**

目標：

- 建立 login request
- 用剛剛建立的 user 登入
- 成功拿到 `access_token`
- 看懂 login response

明天還不一定要自動存 token，可以先手動觀察 response。

你明天直接傳：

**4/30 Postman Day 3 開始**