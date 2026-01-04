# ApproveCommentAPIView - Updated Documentation

## Endpoint
```
POST http://localhost:8000/api/v1/comments/approve
```

## Description
This endpoint changes a comment's status from `WAITING_FOR_APPROVE` to `APPROVED`.
Optionally, you can also update the comment's response text when approving.

## Method
`POST`

## Request Body

### Option 1: Approve Only (No Response Update)
```json
{
  "id": 123
}
```

### Option 2: Approve + Update Response
```json
{
  "id": 123,
  "response": "Thank you for your wonderful feedback! We appreciate your support."
}
```

### Parameters
- **id** (required, integer): The ID of the comment to approve
- **response** (optional, string): New response text to update (if provided)

---

## Success Response

### Status: 200 OK

**Without Response Update:**
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
    "response": "Original AI generated response",
    "status": "APPROVED",
    "is_active": true,
    "created": "2025-12-31T10:30:00Z",
    "modified": "2025-12-31T11:45:00Z"
  }
}
```

**With Response Update:**
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
    "response": "Thank you for your wonderful feedback! We appreciate your support.",
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

### Example 1: Approve Without Updating Response

#### cURL
```bash
curl -X POST http://localhost:8000/api/v1/comments/approve \
  -H "Content-Type: application/json" \
  -d '{"id": 123}'
```

#### Python
```python
import requests

url = 'http://localhost:8000/api/v1/comments/approve'
data = {'id': 123}

response = requests.post(url, json=data)
result = response.json()

if result['status'] == 'true':
    print(f"Comment {data['id']} approved successfully!")
    print(f"Response: {result['payload']['response']}")
```

#### JavaScript
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
    console.log('Response:', data.payload.response);
  }
  
  return data;
};

// Usage
approveComment(123);
```

---

### Example 2: Approve AND Update Response

#### cURL
```bash
curl -X POST http://localhost:8000/api/v1/comments/approve \
  -H "Content-Type: application/json" \
  -d '{
    "id": 123,
    "response": "Thank you for your wonderful feedback! We appreciate your support."
  }'
```

#### Python
```python
import requests

url = 'http://localhost:8000/api/v1/comments/approve'
data = {
    'id': 123,
    'response': 'Thank you for your wonderful feedback! We truly appreciate your support.'
}

response = requests.post(url, json=data)
result = response.json()

if result['status'] == 'true':
    print(f"Comment {data['id']} approved with updated response!")
    print(f"New response: {result['payload']['response']}")
else:
    print(f"Error: {result['message']}")
```

#### JavaScript
```javascript
const approveCommentWithResponse = async (commentId, newResponse) => {
  const response = await fetch('http://localhost:8000/api/v1/comments/approve', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ 
      id: commentId,
      response: newResponse 
    })
  });
  
  const data = await response.json();
  
  if (data.status === 'true') {
    console.log('Comment approved with updated response!');
    console.log('Updated comment:', data.payload);
  } else {
    console.error('Error:', data.message);
  }
  
  return data;
};

// Usage
approveCommentWithResponse(
  123, 
  'Thank you for your wonderful feedback! We appreciate your support.'
);
```

#### Axios
```javascript
import axios from 'axios';

const approveWithCustomResponse = async (commentId, customResponse = null) => {
  try {
    const payload = { id: commentId };
    
    // Add response only if provided
    if (customResponse) {
      payload.response = customResponse;
    }
    
    const response = await axios.post(
      'http://localhost:8000/api/v1/comments/approve',
      payload
    );
    
    if (response.data.status === 'true') {
      console.log('✓ Comment approved successfully!');
      return response.data.payload;
    }
  } catch (error) {
    console.error('✗ Error:', error.response?.data || error.message);
    throw error;
  }
};

// Usage 1: Approve only
approveWithCustomResponse(123);

// Usage 2: Approve with custom response
approveWithCustomResponse(
  123, 
  'Thank you for sharing your experience!'
);
```

---

## Real-World Workflow Examples

### Example 1: Review & Approve with Human Touch
```python
import requests

BASE_URL = 'http://localhost:8000/api/v1/comments'

# Get comments waiting for approval
response = requests.get(
    f'{BASE_URL}/status/filter',
    params={'status': 'WAITING_FOR_APPROVE'}
)
waiting_comments = response.json()['payload']

for comment in waiting_comments:
    print(f"\n{'='*60}")
    print(f"Comment ID: {comment['id']}")
    print(f"Customer: {comment['customer_id']}")
    print(f"Content: {comment['content']}")
    print(f"AI Response: {comment['response']}")
    print('='*60)
    
    # Moderator decides to improve the AI response
    user_decision = input("\nApprove? (y/edit/skip): ").strip().lower()
    
    if user_decision == 'y':
        # Approve without changes
        result = requests.post(
            f'{BASE_URL}/approve',
            json={'id': comment['id']}
        )
        print("✓ Approved with original response")
        
    elif user_decision == 'edit':
        # Edit and approve
        new_response = input("Enter new response: ")
        result = requests.post(
            f'{BASE_URL}/approve',
            json={
                'id': comment['id'],
                'response': new_response
            }
        )
        print("✓ Approved with updated response")
        
    else:
        print("⊘ Skipped")
```

---

### Example 2: Batch Approval with Standard Response
```python
import requests

BASE_URL = 'http://localhost:8000/api/v1/comments'

# Standard professional response template
STANDARD_RESPONSE = "Thank you for taking the time to share your feedback. We truly appreciate your support!"

# Get all waiting comments
response = requests.get(
    f'{BASE_URL}/status/filter',
    params={'status': 'WAITING_FOR_APPROVE'}
)
comments = response.json()['payload']

approved_count = 0
failed_count = 0

for comment in comments:
    # Approve with standard response
    result = requests.post(
        f'{BASE_URL}/approve',
        json={
            'id': comment['id'],
            'response': STANDARD_RESPONSE
        }
    )
    
    if result.json()['status'] == 'true':
        approved_count += 1
        print(f"✓ Comment #{comment['id']} approved")
    else:
        failed_count += 1
        print(f"✗ Comment #{comment['id']} failed: {result.json()['message']}")

print(f"\n{'='*60}")
print(f"Summary: {approved_count} approved, {failed_count} failed")
print('='*60)
```

---

### Example 3: Conditional Response Update
```python
import requests

BASE_URL = 'http://localhost:8000/api/v1/comments'

def approve_comment_smart(comment_id, ai_response, comment_content):
    """
    Approve comment and update response if AI response is too generic
    """
    
    # Check if AI response is generic
    generic_phrases = ['thank you', 'we appreciate', 'grateful']
    is_generic = all(phrase in ai_response.lower() for phrase in generic_phrases)
    
    # Check if comment mentions specific issues
    has_issue = any(word in comment_content.lower() 
                   for word in ['problem', 'issue', 'broken', 'not working'])
    
    payload = {'id': comment_id}
    
    # Update response if needed
    if is_generic and has_issue:
        payload['response'] = (
            "Thank you for bringing this to our attention. "
            "We take all feedback seriously and will look into this matter. "
            "Please feel free to contact our support team for immediate assistance."
        )
    
    # Approve
    response = requests.post(f'{BASE_URL}/approve', json=payload)
    return response.json()

# Usage
comment = {
    'id': 123,
    'content': 'Product is broken, very disappointed',
    'response': 'Thank you for your feedback'
}

result = approve_comment_smart(
    comment['id'], 
    comment['response'], 
    comment['content']
)

print(f"Approved: {result['status']}")
print(f"Final response: {result['payload']['response']}")
```

---

## Use Cases

### 1. **Quick Approval**
Moderator reviews AI response and approves without changes
```json
{"id": 123}
```

### 2. **Response Enhancement**
Moderator improves AI response before approval
```json
{
  "id": 123,
  "response": "Enhanced professional response"
}
```

### 3. **Response Correction**
AI made an error, moderator fixes it
```json
{
  "id": 123,
  "response": "Corrected accurate response"
}
```

### 4. **Personalization**
Add personal touch to generic AI response
```json
{
  "id": 123,
  "response": "Hi John, thank you for your feedback! We're glad you enjoyed the product."
}
```

---

## Notes

1. ✅ **Optional Field**: `response` parameter is completely optional
2. ✅ **Flexible**: Approve only OR approve + update in single request
3. ✅ **Atomic**: Both status and response update happen atomically
4. ✅ **Validation**: Status validation still applies (must be WAITING_FOR_APPROVE)
5. ✅ **Audit Trail**: `modified` timestamp automatically updated on save

---

## Related Endpoints

### Get Comments Waiting for Approval
```bash
GET http://localhost:8000/api/v1/comments/status/filter?status=WAITING_FOR_APPROVE
```

### Update Any Status (Generic)
```bash
POST http://localhost:8000/api/v1/comments/update/answered
Content-Type: application/json

{
  "id": 123,
  "status": "ANY_STATUS"
}
```
