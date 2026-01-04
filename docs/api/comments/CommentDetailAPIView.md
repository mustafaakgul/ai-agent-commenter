# CommentDetailAPIView - API Documentation

## Endpoint
```
GET http://localhost:8000/api/v1/comments/{comment_id}
```

## Description
This endpoint retrieves detailed information about a specific comment including:
- Comment basic information
- Related CommentAnalyzer records (multiple analyzers possible)
- Related CommentQualityScore (one-to-one relationship)

## Method
`GET`

## URL Parameters
- **comment_id** (required, integer): The ID of the comment to retrieve

---

## Success Response

### Status: 200 OK

```json
{
  "status": "true",
  "message": "Comment details retrieved successfully",
  "payload": {
    "id": 123,
    "customer_id": "CUST001",
    "product_name": "Wireless Headphones",
    "content_id": "CONT001",
    "content": "Great product! The sound quality is amazing and battery life is excellent.",
    "web_url": "https://example.com/review/123",
    "response": "Thank you for your wonderful feedback! We're thrilled to hear you're enjoying the sound quality and battery life.",
    "status": "APPROVED",
    "is_active": true,
    "created": "2026-01-01T10:30:00Z",
    "modified": "2026-01-02T14:20:00Z",
    
    "analyzers": [
      {
        "id": 1,
        "analyzed_at": "2026-01-01T10:31:00Z",
        "sentiment": "positive",
        "sentiment_score": 0.92,
        "category": "Product Quality",
        "urgency": "low",
        "keywords": "sound quality, battery life, amazing, excellent",
        "summary": "Customer is very satisfied with product quality",
        "main_issue": "None - positive feedback",
        "required_action": false,
        "response_tone": "appreciative",
        "response": "Thank you for your wonderful feedback!",
        "quality_control": "Passed all quality checks",
        "created": "2026-01-01T10:31:00Z",
        "modified": "2026-01-01T10:31:00Z"
      }
    ],
    
    "quality_score": {
      "id": 1,
      "professionalism": 95,
      "relevance": 90,
      "warmth": 88,
      "solution_focus": 85,
      "overall": 90,
      "feedback": "Excellent response with good balance of professionalism and warmth",
      "approved": true,
      "created": "2026-01-01T10:32:00Z",
      "modified": "2026-01-01T10:32:00Z"
    }
  }
}
```

---

## Response Without Analyzers or Quality Score

If a comment doesn't have related analyzers or quality scores:

```json
{
  "status": "true",
  "message": "Comment details retrieved successfully",
  "payload": {
    "id": 456,
    "customer_id": "CUST002",
    "product_name": "Smart Watch",
    "content_id": "CONT002",
    "content": "Just received the product",
    "web_url": "https://example.com/review/456",
    "response": "temp",
    "status": "WAITING_FOR_ANSWER",
    "is_active": true,
    "created": "2026-01-02T15:00:00Z",
    "modified": "2026-01-02T15:00:00Z",
    
    "analyzers": [],
    "quality_score": null
  }
}
```

---

## Error Responses

### 1. Comment Not Found
**Status: 404 Not Found**
```json
{
  "status": "false",
  "message": "Comment not found",
  "payload": {}
}
```

---

## Usage Examples

### Example 1: Get Comment Details

#### cURL
```bash
curl -X GET http://localhost:8000/api/v1/comments/123
```

#### Python (requests)
```python
import requests

comment_id = 123
url = f'http://localhost:8000/api/v1/comments/{comment_id}'

response = requests.get(url)
result = response.json()

if result['status'] == 'true':
    comment = result['payload']
    print(f"Comment ID: {comment['id']}")
    print(f"Content: {comment['content']}")
    print(f"Response: {comment['response']}")
    print(f"Status: {comment['status']}")
    
    # Check analyzers
    if comment['analyzers']:
        print(f"\nFound {len(comment['analyzers'])} analyzer(s)")
        for analyzer in comment['analyzers']:
            print(f"  - Sentiment: {analyzer['sentiment']} ({analyzer['sentiment_score']})")
            print(f"  - Category: {analyzer['category']}")
            print(f"  - Urgency: {analyzer['urgency']}")
    
    # Check quality score
    if comment['quality_score']:
        quality = comment['quality_score']
        print(f"\nQuality Score: {quality['overall']}/100")
        print(f"  - Professionalism: {quality['professionalism']}")
        print(f"  - Relevance: {quality['relevance']}")
        print(f"  - Warmth: {quality['warmth']}")
        print(f"  - Solution Focus: {quality['solution_focus']}")
        print(f"  - Approved: {quality['approved']}")
else:
    print(f"Error: {result['message']}")
```

#### JavaScript (Fetch)
```javascript
const getCommentDetails = async (commentId) => {
  try {
    const response = await fetch(`http://localhost:8000/api/v1/comments/${commentId}`);
    const data = await response.json();
    
    if (data.status === 'true') {
      const comment = data.payload;
      console.log('Comment Details:', comment);
      
      // Display analyzers
      if (comment.analyzers && comment.analyzers.length > 0) {
        console.log('\nAnalyzers:');
        comment.analyzers.forEach(analyzer => {
          console.log(`  Sentiment: ${analyzer.sentiment} (${analyzer.sentiment_score})`);
          console.log(`  Category: ${analyzer.category}`);
          console.log(`  Urgency: ${analyzer.urgency}`);
        });
      }
      
      // Display quality score
      if (comment.quality_score) {
        console.log('\nQuality Score:');
        console.log(`  Overall: ${comment.quality_score.overall}/100`);
        console.log(`  Professionalism: ${comment.quality_score.professionalism}`);
        console.log(`  Approved: ${comment.quality_score.approved}`);
      }
      
      return comment;
    } else {
      console.error('Error:', data.message);
      return null;
    }
  } catch (error) {
    console.error('Request failed:', error);
    throw error;
  }
};

// Usage
getCommentDetails(123);
```

#### Axios
```javascript
import axios from 'axios';

const fetchCommentDetails = async (commentId) => {
  try {
    const response = await axios.get(
      `http://localhost:8000/api/v1/comments/${commentId}`
    );
    
    if (response.data.status === 'true') {
      return response.data.payload;
    } else {
      throw new Error(response.data.message);
    }
  } catch (error) {
    console.error('Error fetching comment details:', error.message);
    throw error;
  }
};

// Usage
fetchCommentDetails(123)
  .then(comment => {
    console.log('Comment:', comment);
    console.log('Analyzers:', comment.analyzers);
    console.log('Quality Score:', comment.quality_score);
  })
  .catch(error => console.error(error));
```

---

## Real-World Use Cases

### Use Case 1: Display Comment Card with Analysis
```python
import requests

def display_comment_card(comment_id):
    url = f'http://localhost:8000/api/v1/comments/{comment_id}'
    response = requests.get(url)
    
    if response.json()['status'] == 'true':
        comment = response.json()['payload']
        
        print("=" * 60)
        print(f"COMMENT #{comment['id']}")
        print("=" * 60)
        print(f"Customer: {comment['customer_id']}")
        print(f"Product: {comment['product_name']}")
        print(f"Status: {comment['status']}")
        print(f"\nOriginal Comment:")
        print(f"  {comment['content']}")
        print(f"\nOur Response:")
        print(f"  {comment['response']}")
        
        # Show analysis
        if comment['analyzers']:
            analyzer = comment['analyzers'][0]  # Get first analyzer
            print(f"\n--- AI Analysis ---")
            print(f"Sentiment: {analyzer['sentiment']} ({analyzer['sentiment_score']:.2f})")
            print(f"Category: {analyzer['category']}")
            print(f"Urgency: {analyzer['urgency']}")
            print(f"Keywords: {analyzer['keywords']}")
            print(f"Summary: {analyzer['summary']}")
        
        # Show quality metrics
        if comment['quality_score']:
            quality = comment['quality_score']
            print(f"\n--- Quality Metrics ---")
            print(f"Overall Score: {quality['overall']}/100")
            print(f"  Professionalism: {quality['professionalism']}/100")
            print(f"  Relevance: {quality['relevance']}/100")
            print(f"  Warmth: {quality['warmth']}/100")
            print(f"  Solution Focus: {quality['solution_focus']}/100")
            print(f"Status: {'✓ Approved' if quality['approved'] else '✗ Pending'}")
            if quality['feedback']:
                print(f"Feedback: {quality['feedback']}")
        
        print("=" * 60)
    else:
        print(f"Error: Comment {comment_id} not found")

# Usage
display_comment_card(123)
```

---

### Use Case 2: Quality Dashboard
```python
import requests

def analyze_comment_quality(comment_ids):
    """Analyze multiple comments and show quality statistics"""
    
    results = []
    for comment_id in comment_ids:
        url = f'http://localhost:8000/api/v1/comments/{comment_id}'
        response = requests.get(url)
        
        if response.json()['status'] == 'true':
            comment = response.json()['payload']
            
            quality_data = {
                'id': comment['id'],
                'product': comment['product_name'],
                'status': comment['status'],
                'has_analyzer': len(comment['analyzers']) > 0,
                'has_quality_score': comment['quality_score'] is not None
            }
            
            if comment['quality_score']:
                quality_data.update({
                    'overall_score': comment['quality_score']['overall'],
                    'approved': comment['quality_score']['approved']
                })
            
            if comment['analyzers']:
                analyzer = comment['analyzers'][0]
                quality_data.update({
                    'sentiment': analyzer['sentiment'],
                    'urgency': analyzer['urgency']
                })
            
            results.append(quality_data)
    
    # Display statistics
    print("\n=== QUALITY DASHBOARD ===\n")
    
    total = len(results)
    with_quality = sum(1 for r in results if r.get('has_quality_score'))
    approved = sum(1 for r in results if r.get('approved'))
    
    print(f"Total Comments: {total}")
    print(f"With Quality Scores: {with_quality} ({with_quality/total*100:.1f}%)")
    print(f"Approved: {approved} ({approved/total*100:.1f}%)")
    
    if results:
        avg_score = sum(r.get('overall_score', 0) for r in results) / len([r for r in results if 'overall_score' in r])
        print(f"Average Quality Score: {avg_score:.1f}/100")
    
    print("\n--- Individual Comments ---")
    for r in results:
        status_icon = "✓" if r.get('approved') else "⊗"
        score = r.get('overall_score', 'N/A')
        print(f"{status_icon} Comment #{r['id']}: {r['product']} - Score: {score}")

# Usage
comment_ids = [123, 124, 125, 126]
analyze_comment_quality(comment_ids)
```

---

### Use Case 3: Sentiment Analysis Report
```python
import requests
from collections import Counter

def sentiment_report(comment_ids):
    """Generate sentiment analysis report"""
    
    sentiments = []
    urgencies = []
    categories = []
    
    for comment_id in comment_ids:
        url = f'http://localhost:8000/api/v1/comments/{comment_id}'
        response = requests.get(url)
        
        if response.json()['status'] == 'true':
            comment = response.json()['payload']
            
            if comment['analyzers']:
                analyzer = comment['analyzers'][0]
                sentiments.append(analyzer['sentiment'])
                urgencies.append(analyzer['urgency'])
                categories.append(analyzer['category'])
    
    print("\n=== SENTIMENT ANALYSIS REPORT ===\n")
    
    print("Sentiment Distribution:")
    for sentiment, count in Counter(sentiments).items():
        print(f"  {sentiment}: {count} ({count/len(sentiments)*100:.1f}%)")
    
    print("\nUrgency Levels:")
    for urgency, count in Counter(urgencies).items():
        print(f"  {urgency}: {count}")
    
    print("\nTop Categories:")
    for category, count in Counter(categories).most_common(5):
        print(f"  {category}: {count}")

# Usage
comment_ids = range(1, 101)  # Analyze comments 1-100
sentiment_report(comment_ids)
```

---

## Response Structure

### Main Comment Fields
- `id`: Comment ID
- `customer_id`: Customer identifier
- `product_name`: Product name
- `content_id`: Content identifier
- `content`: Original comment text
- `web_url`: URL where comment was posted
- `response`: AI-generated or manual response
- `status`: Current status (WAITING_FOR_ANSWER, WAITING_FOR_APPROVE, APPROVED, etc.)
- `is_active`: Whether comment is active
- `created`: Creation timestamp
- `modified`: Last modification timestamp

### Analyzers Array (Multiple)
Each analyzer contains:
- `sentiment`: Sentiment classification
- `sentiment_score`: Numeric sentiment score
- `category`: Comment category
- `urgency`: Urgency level
- `keywords`: Extracted keywords
- `summary`: Analysis summary
- `main_issue`: Main issue identified
- `required_action`: Whether action is required
- `response_tone`: Recommended response tone

### Quality Score Object (One-to-One)
- `professionalism`: Score 0-100
- `relevance`: Score 0-100
- `warmth`: Score 0-100
- `solution_focus`: Score 0-100
- `overall`: Overall score 0-100
- `feedback`: Quality feedback text
- `approved`: Approval status

---

## Performance Notes

- Uses `prefetch_related` for optimal database query performance
- Single database query retrieves comment with all related data
- Nested serializers automatically handle related objects
- Returns empty array `[]` for analyzers if none exist
- Returns `null` for quality_score if doesn't exist

---

## Related Endpoints

### List All Comments
```bash
GET http://localhost:8000/api/v1/comments/
```

### Filter Comments by Status
```bash
GET http://localhost:8000/api/v1/comments/status/filter?status=APPROVED
```

### Approve Comment
```bash
POST http://localhost:8000/api/v1/comments/approve
```
