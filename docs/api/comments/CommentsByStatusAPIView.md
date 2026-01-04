# CommentsByStatusAPIView - API Endpoint Documentation

## Base URL
```
http://localhost:8000/api/v1/comments/status/filter
```

## Method
`GET`

## Query Parameters
- **status** (required): Comment status to filter by

## Available Status Values
- `WAITING_FOR_ANSWER`
- `WAITING_FOR_APPROVE`
- `APPROVED`
- `ANSWERED`
- `REPORTED`
- `REJECTED`
- `ERROR`

---

## Example Requests

### 1. Get all APPROVED comments
```bash
GET http://localhost:8000/api/v1/comments/status/filter?status=APPROVED
```

**cURL:**
```bash
curl -X GET "http://localhost:8000/api/v1/comments/status/filter?status=APPROVED"
```

**Response (200 OK):**
```json
{
  "status": "true",
  "message": "successful",
  "payload": [
    {
      "id": 1,
      "customer_id": "CUST001",
      "product_name": "Product Name",
      "content_id": "CONT001",
      "content": "Great product!",
      "web_url": "https://example.com/review/1",
      "response": "Thank you for your feedback",
      "status": "APPROVED",
      "is_active": true,
      "created": "2025-12-28T10:30:00Z",
      "modified": "2025-12-28T10:30:00Z"
    },
    {
      "id": 2,
      "customer_id": "CUST002",
      "product_name": "Another Product",
      "content_id": "CONT002",
      "content": "Excellent service!",
      "web_url": "https://example.com/review/2",
      "response": "We appreciate your kind words",
      "status": "APPROVED",
      "is_active": true,
      "created": "2025-12-28T11:15:00Z",
      "modified": "2025-12-28T11:15:00Z"
    }
  ]
}
```

---

### 2. Get all WAITING_FOR_ANSWER comments
```bash
GET http://localhost:8000/api/v1/comments/status/filter?status=WAITING_FOR_ANSWER
```

**cURL:**
```bash
curl -X GET "http://localhost:8000/api/v1/comments/status/filter?status=WAITING_FOR_ANSWER"
```

---

### 3. Get all REJECTED comments
```bash
GET http://localhost:8000/api/v1/comments/status/filter?status=REJECTED
```

**cURL:**
```bash
curl -X GET "http://localhost:8000/api/v1/comments/status/filter?status=REJECTED"
```

---

### 4. Get all ANSWERED comments
```bash
GET http://localhost:8000/api/v1/comments/status/filter?status=ANSWERED
```

**cURL:**
```bash
curl -X GET "http://localhost:8000/api/v1/comments/status/filter?status=ANSWERED"
```

---

### 5. Get all ERROR status comments
```bash
GET http://localhost:8000/api/v1/comments/status/filter?status=ERROR
```

**cURL:**
```bash
curl -X GET "http://localhost:8000/api/v1/comments/status/filter?status=ERROR"
```

---

## Error Cases

### Missing status parameter
**Request:**
```bash
GET http://localhost:8000/api/v1/comments/status/filter
```

**Response (400 Bad Request):**
```json
{
  "status": "false",
  "message": "Status parameter is required",
  "payload": {}
}
```

---

### Empty result (no matching comments)
**Request:**
```bash
GET http://localhost:8000/api/v1/comments/status/filter?status=REPORTED
```

**Response (200 OK):**
```json
{
  "status": "true",
  "message": "successful",
  "payload": []
}
```

---

## Python Requests Examples

### Using Python requests library:
```python
import requests

# Example 1: Get approved comments
response = requests.get(
    'http://localhost:8000/api/v1/comments/status/filter',
    params={'status': 'APPROVED'}
)
data = response.json()
print(data)

# Example 2: Get waiting for answer comments
response = requests.get(
    'http://localhost:8000/api/v1/comments/status/filter',
    params={'status': 'WAITING_FOR_ANSWER'}
)
data = response.json()
print(f"Found {len(data['payload'])} comments")

# Example 3: Get rejected comments
response = requests.get(
    'http://localhost:8000/api/v1/comments/status/filter?status=REJECTED'
)
data = response.json()
for comment in data['payload']:
    print(f"Comment ID: {comment['id']}, Status: {comment['status']}")
```

---

## JavaScript/Fetch Examples

### Using Fetch API:
```javascript
// Example 1: Get approved comments
fetch('http://localhost:8000/api/v1/comments/status/filter?status=APPROVED')
  .then(response => response.json())
  .then(data => {
    console.log('Approved comments:', data.payload);
  });

// Example 2: Get waiting comments with async/await
async function getWaitingComments() {
  const response = await fetch(
    'http://localhost:8000/api/v1/comments/status/filter?status=WAITING_FOR_ANSWER'
  );
  const data = await response.json();
  return data.payload;
}

// Example 3: Get any status
async function getCommentsByStatus(status) {
  const url = new URL('http://localhost:8000/api/v1/comments/status/filter');
  url.searchParams.append('status', status);
  
  const response = await fetch(url);
  const data = await response.json();
  
  if (data.status === 'true') {
    return data.payload;
  } else {
    throw new Error(data.message);
  }
}

// Usage
getCommentsByStatus('APPROVED').then(comments => {
  console.log(`Found ${comments.length} approved comments`);
});
```

---

## Postman Collection Example

**Request Name:** Get Comments by Status  
**Method:** GET  
**URL:** `{{base_url}}/api/v1/comments/status/filter`  
**Params:**
- Key: `status`
- Value: `APPROVED` (or any valid status)

**Environment Variables:**
```json
{
  "base_url": "http://localhost:8000"
}
```

---

## Notes

1. **Case Sensitivity:** Status parameter is case-sensitive. Use uppercase (e.g., `APPROVED`, not `approved`)
2. **Empty Results:** If no comments match the status, an empty array is returned (not an error)
3. **Invalid Status:** Invalid status values return empty results, not an error
4. **All Comments:** This endpoint filters by status. To get all comments regardless of status, use the base endpoint: `GET /api/v1/comments/`
