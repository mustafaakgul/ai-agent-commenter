# ApproveCommentAPIView - API Documentation

## Endpoint
```
POST http://localhost:8000/api/v1/comments/approve
```

## Description
This endpoint changes a comment's status from `WAITING_FOR_APPROVE` to `APPROVED`.

## Method
`POST`

## Request Body
```json
{
  "id": 123
}
```

### Parameters
- **id** (required, integer): The ID of the comment to approve

---

## Success Response

### Status: 200 OK
```json
{
  "status": "true",
  "message": "Comment approved successfully",
  "payload": {
    "id": 123,
    "customer_id": "CUST001",
    "product_name": "Product Name",
    "content_id": "CONT001",
    "content": "This is a great product!",
    "web_url": "https://example.com/review/123",
    "response": "Thank you for your feedback",
    "status": "APPROVED",
    "is_active": true,
    "created": "2025-12-31T10:30:00Z",
    "modified": "2025-12-31T11:45:00Z"
  }
}
```

---

## Error Responses

### 1. Missing Comment ID
**Status: 400 Bad Request**
```json
{
  "status": "false",
  "message": "Comment ID is required",
  "payload": {}
}
```

### 2. Comment Not Found
**Status: 404 Not Found**
```json
{
  "status": "false",
  "message": "Comment not found",
  "payload": {}
}
```

### 3. Invalid Status (Not WAITING_FOR_APPROVE)
**Status: 400 Bad Request**
```json
{
  "status": "false",
  "message": "Comment status must be WAITING_FOR_APPROVE. Current status: APPROVED",
  "payload": {}
}
```

---

## Usage Examples

### cURL
```bash
curl -X POST http://localhost:8000/api/v1/comments/approve \
  -H "Content-Type: application/json" \
  -d '{"id": 123}'
```

### Python (requests)
```python
import requests

url = 'http://localhost:8000/api/v1/comments/approve'
data = {'id': 123}

response = requests.post(url, json=data)
result = response.json()

if result['status'] == 'true':
    print(f"Comment {data['id']} approved successfully!")
    print(f"New status: {result['payload']['status']}")
else:
    print(f"Error: {result['message']}")
```

### JavaScript (Fetch)
```javascript
const approveComment = async (commentId) => {
  const response = await fetch('http://localhost:8000/api/v1/comments/approve', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ id: commentId })
  });
  
  const data = await response.json();
  
  if (data.status === 'true') {
    console.log('Comment approved successfully!');
    console.log('Updated comment:', data.payload);
  } else {
    console.error('Error:', data.message);
  }
  
  return data;
};

// Usage
approveComment(123);
```

### Axios
```javascript
import axios from 'axios';

const approveComment = async (commentId) => {
  try {
    const response = await axios.post(
      'http://localhost:8000/api/v1/comments/approve',
      { id: commentId }
    );
    
    if (response.data.status === 'true') {
      console.log('Comment approved successfully!');
      return response.data.payload;
    }
  } catch (error) {
    console.error('Error approving comment:', error.response?.data || error.message);
    throw error;
  }
};

// Usage
approveComment(123)
  .then(comment => console.log('Approved comment:', comment))
  .catch(err => console.error(err));
```

---

## Workflow Example

### Complete Approval Workflow
```python
import requests

BASE_URL = 'http://localhost:8000/api/v1/comments'

# Step 1: Get all comments waiting for approval
response = requests.get(f'{BASE_URL}/status/filter', params={'status': 'WAITING_FOR_APPROVE'})
waiting_comments = response.json()['payload']

print(f"Found {len(waiting_comments)} comments waiting for approval")

# Step 2: Review and approve each comment
for comment in waiting_comments:
    print(f"\nReviewing comment #{comment['id']}")
    print(f"Content: {comment['content']}")
    print(f"Response: {comment['response']}")
    
    # Approve the comment
    approve_response = requests.post(
        f'{BASE_URL}/approve',
        json={'id': comment['id']}
    )
    
    result = approve_response.json()
    if result['status'] == 'true':
        print(f"✓ Comment #{comment['id']} approved successfully")
    else:
        print(f"✗ Failed to approve comment #{comment['id']}: {result['message']}")

# Step 3: Verify approved comments
approved_response = requests.get(f'{BASE_URL}/status/filter', params={'status': 'APPROVED'})
approved_comments = approved_response.json()['payload']
print(f"\nTotal approved comments: {len(approved_comments)}")
```

---

## Business Logic

### Status Validation
- Only comments with status `WAITING_FOR_APPROVE` can be approved
- If comment has any other status, a 400 error is returned with current status info
- After approval, status is changed to `APPROVED`

### Use Cases
1. **Content Moderation**: Moderator reviews AI-generated responses before publishing
2. **Quality Control**: Ensure responses meet quality standards
3. **Approval Workflow**: Multi-step approval process for comments
4. **Compliance Check**: Verify responses comply with company policies

---

## Related Endpoints

### Get Comments Waiting for Approval
```bash
GET http://localhost:8000/api/v1/comments/status/filter?status=WAITING_FOR_APPROVE
```

### Get All Approved Comments
```bash
GET http://localhost:8000/api/v1/comments/status/filter?status=APPROVED
```

### Update Comment Status (Generic)
```bash
POST http://localhost:8000/api/v1/comments/update/answered
Content-Type: application/json

{
  "id": 123,
  "status": "ANY_STATUS"
}
```

---

## Notes

1. **Idempotency**: Calling this endpoint on an already approved comment will return an error
2. **Atomic Operation**: Status update is atomic (either succeeds or fails completely)
3. **Audit Trail**: The `modified` timestamp is automatically updated
4. **Validation**: Status validation prevents accidental status changes
