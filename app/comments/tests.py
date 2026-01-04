from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from app.comments.models import Comment


# cd {PROJECT_PATH}/aia/comm && python manage.py test app.comments.tests.CommentsByStatusAPIViewTestCase
class CommentsByStatusAPIViewTestCase(APITestCase):
    """
    Test cases for CommentsByStatusAPIView endpoint

    Test Scenarios:
    1. Success: Valid status parameter with matching comments
    2. Success: Valid status parameter with no matching comments (empty list)
    3. Error: Missing status parameter
    4. Error: Invalid status parameter (not in AGENT_STATUS choices)
    5. Success: Multiple comments with same status
    6. Success: Case sensitivity check
    """

    def setUp(self):
        """Set up test data before each test"""
        self.url = reverse('comments_by_status')

        # Create test comments with different statuses
        self.comment_approved_1 = Comment.objects.create(
            customer_id="CUST001",
            product_name="Test Product 1",
            content_id="CONT001",
            content="This is an approved comment",
            web_url="https://example.com/1",
            status="APPROVED"
        )

        self.comment_approved_2 = Comment.objects.create(
            customer_id="CUST002",
            product_name="Test Product 2",
            content_id="CONT002",
            content="Another approved comment",
            web_url="https://example.com/2",
            status="APPROVED"
        )

        self.comment_waiting = Comment.objects.create(
            customer_id="CUST003",
            product_name="Test Product 3",
            content_id="CONT003",
            content="Waiting for answer",
            web_url="https://example.com/3",
            status="WAITING_FOR_ANSWER"
        )

        self.comment_rejected = Comment.objects.create(
            customer_id="CUST004",
            product_name="Test Product 4",
            content_id="CONT004",
            content="Rejected comment",
            web_url="https://example.com/4",
            status="REJECTED"
        )

        self.comment_answered = Comment.objects.create(
            customer_id="CUST005",
            product_name="Test Product 5",
            content_id="CONT005",
            content="Answered comment",
            web_url="https://example.com/5",
            status="ANSWERED"
        )

    def test_get_comments_by_status_approved_success(self):
        """Test Case 1: Successfully retrieve APPROVED comments"""
        response = self.client.get(self.url, {'status': 'APPROVED'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'true')
        self.assertEqual(response.data['message'], 'successful')
        self.assertEqual(len(response.data['payload']), 2)

        # Verify the correct comments are returned
        comment_ids = [comment['id'] for comment in response.data['payload']]
        self.assertIn(self.comment_approved_1.id, comment_ids)
        self.assertIn(self.comment_approved_2.id, comment_ids)

    def test_get_comments_by_status_waiting_for_answer_success(self):
        """Test Case 2: Successfully retrieve WAITING_FOR_ANSWER comments"""
        response = self.client.get(self.url, {'status': 'WAITING_FOR_ANSWER'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'true')
        self.assertEqual(len(response.data['payload']), 1)
        self.assertEqual(response.data['payload'][0]['id'], self.comment_waiting.id)

    def test_get_comments_by_status_rejected_success(self):
        """Test Case 3: Successfully retrieve REJECTED comments"""
        response = self.client.get(self.url, {'status': 'REJECTED'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['payload']), 1)
        self.assertEqual(response.data['payload'][0]['id'], self.comment_rejected.id)

    def test_get_comments_by_status_answered_success(self):
        """Test Case 4: Successfully retrieve ANSWERED comments"""
        response = self.client.get(self.url, {'status': 'ANSWERED'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['payload']), 1)
        self.assertEqual(response.data['payload'][0]['id'], self.comment_answered.id)

    def test_get_comments_by_status_empty_result(self):
        """Test Case 5: Valid status with no matching comments returns empty list"""
        response = self.client.get(self.url, {'status': 'REPORTED'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'true')
        self.assertEqual(response.data['message'], 'successful')
        self.assertEqual(len(response.data['payload']), 0)
        self.assertIsInstance(response.data['payload'], list)

    def test_get_comments_by_status_missing_parameter(self):
        """Test Case 6: Missing status parameter returns 400 error"""
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['status'], 'false')
        self.assertEqual(response.data['message'], 'Status parameter is required')
        self.assertEqual(response.data['payload'], {})

    def test_get_comments_by_status_empty_parameter(self):
        """Test Case 7: Empty status parameter returns 400 error"""
        response = self.client.get(self.url, {'status': ''})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['status'], 'false')
        self.assertEqual(response.data['message'], 'Status parameter is required')

    def test_get_comments_by_status_invalid_status(self):
        """Test Case 8: Invalid status parameter (not in AGENT_STATUS)"""
        response = self.client.get(self.url, {'status': 'INVALID_STATUS'})

        # Should return 200 with empty list (no matching records)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['payload']), 0)

    def test_get_comments_by_status_case_sensitive(self):
        """Test Case 9: Status parameter is case-sensitive"""
        # Lowercase should not match
        response = self.client.get(self.url, {'status': 'approved'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['payload']), 0)

    def test_get_comments_by_status_multiple_approved_comments(self):
        """Test Case 10: Multiple comments with same status are all returned"""
        # Create additional approved comments
        for i in range(3):
            Comment.objects.create(
                customer_id=f"CUST00{6+i}",
                product_name=f"Test Product {6+i}",
                content_id=f"CONT00{6+i}",
                content=f"Additional approved comment {i}",
                web_url=f"https://example.com/{6+i}",
                status="APPROVED"
            )

        response = self.client.get(self.url, {'status': 'APPROVED'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # 2 from setUp + 3 new = 5 total
        self.assertEqual(len(response.data['payload']), 5)

    def test_get_comments_by_status_waiting_for_approve(self):
        """Test Case 11: Successfully retrieve WAITING_FOR_APPROVE comments"""
        comment = Comment.objects.create(
            customer_id="CUST100",
            product_name="Test Product",
            content_id="CONT100",
            content="Waiting for approve",
            web_url="https://example.com/100",
            status="WAITING_FOR_APPROVE"
        )

        response = self.client.get(self.url, {'status': 'WAITING_FOR_APPROVE'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['payload']), 1)
        self.assertEqual(response.data['payload'][0]['id'], comment.id)

    def test_get_comments_by_status_error(self):
        """Test Case 12: Successfully retrieve ERROR status comments"""
        comment = Comment.objects.create(
            customer_id="CUST101",
            product_name="Test Product",
            content_id="CONT101",
            content="Error comment",
            web_url="https://example.com/101",
            status="ERROR"
        )

        response = self.client.get(self.url, {'status': 'ERROR'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['payload']), 1)
        self.assertEqual(response.data['payload'][0]['id'], comment.id)

    def test_get_comments_response_structure(self):
        """Test Case 13: Verify response structure is correct"""
        response = self.client.get(self.url, {'status': 'APPROVED'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check response structure
        self.assertIn('status', response.data)
        self.assertIn('message', response.data)
        self.assertIn('payload', response.data)

        # Check payload structure
        if len(response.data['payload']) > 0:
            comment = response.data['payload'][0]
            self.assertIn('id', comment)
            self.assertIn('customer_id', comment)
            self.assertIn('product_name', comment)
            self.assertIn('content', comment)
            self.assertIn('status', comment)
            self.assertIn('web_url', comment)

    def test_get_comments_by_status_with_inactive_comments(self):
        """Test Case 14: Verify inactive comments are also returned if status matches"""
        inactive_comment = Comment.objects.create(
            customer_id="CUST200",
            product_name="Test Product",
            content_id="CONT200",
            content="Inactive approved comment",
            web_url="https://example.com/200",
            status="APPROVED",
            is_active=False
        )

        response = self.client.get(self.url, {'status': 'APPROVED'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Should include inactive comments
        comment_ids = [comment['id'] for comment in response.data['payload']]
        self.assertIn(inactive_comment.id, comment_ids)

    def tearDown(self):
        """Clean up after each test"""
        Comment.objects.all().delete()
