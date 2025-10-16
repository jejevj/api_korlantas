Here’s the markdown for all the requests in the provided JSON collection, structured for easy readability. I’ve included the details for each request like method, URL, headers, body, and tests.

---

# Korlantas API Collection

## 1. **Authentication**

### 1.1. **Login First**

* **Method**: POST
* **URL**: `{{base_url}}api/v1/auth/login`
* **Body** (raw JSON):

  ```json
  {
    "username": "tantri",
    "password": "tantri"
  }
  ```
* **Tests** (extract and store token):

  ```javascript
  let jsonData = pm.response.json();
  pm.environment.set("auth_token", jsonData.data.token);
  ```

---

### 1.2. **Logout**

* **Method**: POST
* **URL**: `{{base_url}}api/v1/auth/logout`
* **Headers**:

  * `Authorization: Bearer {{auth_token}}`

---

## 2. **CFD**

### 2.1. **CFD Get (Latest)**

* **Method**: POST
* **URL**: `{{base_url}}api/v1/cfd/latest`
* **Headers**:

  * `Authorization: Bearer {{auth_token}}`
* **Body** (raw JSON):

  ```json
  {
    "changed_by": "tantri",
    "valid_content": "f",  // 't' for True, 'f' for False
    "page": 1,
    "per_page": 5
  }
  ```

---

### 2.2. **Post CFD**

* **Method**: POST
* **URL**: `{{base_url}}api/v1/cfd`
* **Headers**:

  * `Authorization: Bearer {{auth_token}}`
* **Body** (form-data):

  * `valid_content`: `true`
  * `jenis_ranmor`: `1`
  * `nomor_rangka`: `12345678901234567`
  * `nomor_mesin`: `12345678901234567`
  * `plat_nomor`: `BH 2222 KK`
  * `nomor_rangka_pic`: *(file)*
  * `nomor_mesin_pic`: *(file)*
  * `tampak_depan_pic`: *(file)*
  * `tampak_belakang_pic`: *(file)*
  * `company_id`: `60`
  * `changed_by`: `tantri`
  * `location_id`: `50`

---

## 3. **Restricted Action**

### 3.1. **Restricted Action Get**

* **Method**: GET
* **URL**: `{{base_url}}api/v1/protected`
* **Headers**:

  * `Authorization: Bearer {{auth_token}}`

---

### Usage Instructions:

1. **Set Up Environment Variables in Postman**:

   * Create an environment variable `base_url` with the value `http://178.248.73.51:10980/`.
   * Create an environment variable `auth_token` to store the token after login.

2. **Capture Token**:

   * After the **Login First** request, the token will be captured and saved to `auth_token` using the **Tests** tab.

3. **Use Token in Requests**:

   * For all other requests requiring authentication (like `CFD Get`, `Post CFD`), the token is automatically used via the `Authorization: Bearer {{auth_token}}` header.

---

Let me know if you need any modifications or further help!
