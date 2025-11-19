"""
API tests for the notification service.
"""

import unittest
import json
import os
from unittest.mock import patch, MagicMock
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app


class NotificationAPITestCase(unittest.TestCase):
    """Test cases for notification API endpoints."""
    
    def setUp(self):
        """Set up test client."""
        self.app = app.test_client()
        self.app.testing = True
    
    def test_health_check(self):
        """Test health check endpoint."""
        response = self.app.get('/api/health')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'healthy')
        self.assertEqual(data['service'], 'notification-service')
    
    @patch('token_manager.save_token')
    def test_register_token_success(self, mock_save_token):
        """Test successful token registration."""
        mock_save_token.return_value = {
            'token': 'test_token',
            'app_id': 'test-app',
            'user_id': 'user123'
        }
        
        response = self.app.post(
            '/api/register-token',
            data=json.dumps({
                'token': 'test_token',
                'app_id': 'test-app',
                'user_id': 'user123'
            }),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertEqual(data['app_id'], 'test-app')
    
    def test_register_token_missing_token(self):
        """Test token registration with missing token."""
        response = self.app.post(
            '/api/register-token',
            data=json.dumps({
                'app_id': 'test-app'
            }),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertFalse(data['success'])
        self.assertIn('token is required', data['error'])
    
    def test_register_token_missing_app_id(self):
        """Test token registration with missing app_id."""
        response = self.app.post(
            '/api/register-token',
            data=json.dumps({
                'token': 'test_token'
            }),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertFalse(data['success'])
        self.assertIn('app_id is required', data['error'])
    
    @patch('firebase_service.send_push_notification')
    def test_send_notification_success(self, mock_send):
        """Test successful notification send."""
        mock_send.return_value = 'projects/test/messages/123'
        
        response = self.app.post(
            '/api/send-notification',
            data=json.dumps({
                'token': 'test_token',
                'title': 'Test Title',
                'body': 'Test Body',
                'app_id': 'test-app'
            }),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertIn('message_id', data)
    
    def test_send_notification_missing_fields(self):
        """Test notification send with missing required fields."""
        # Missing title
        response = self.app.post(
            '/api/send-notification',
            data=json.dumps({
                'token': 'test_token',
                'body': 'Test Body'
            }),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertFalse(data['success'])
        self.assertIn('title is required', data['error'])
    
    @patch('token_manager.get_tokens_for_app')
    @patch('firebase_service.send_multicast_notification')
    def test_send_to_app_success(self, mock_send_multicast, mock_get_tokens):
        """Test successful send to app."""
        mock_get_tokens.return_value = ['token1', 'token2', 'token3']
        mock_response = MagicMock()
        mock_response.success_count = 3
        mock_response.failure_count = 0
        mock_send_multicast.return_value = mock_response
        
        response = self.app.post(
            '/api/send-to-app',
            data=json.dumps({
                'app_id': 'test-app',
                'title': 'Test Title',
                'body': 'Test Body'
            }),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertEqual(data['sent_to'], 3)
        self.assertEqual(data['app_id'], 'test-app')
    
    @patch('token_manager.get_tokens_for_app')
    def test_send_to_app_no_tokens(self, mock_get_tokens):
        """Test send to app when no tokens exist."""
        mock_get_tokens.return_value = []
        
        response = self.app.post(
            '/api/send-to-app',
            data=json.dumps({
                'app_id': 'test-app',
                'title': 'Test Title',
                'body': 'Test Body'
            }),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertEqual(data['sent_to'], 0)
    
    def test_send_to_app_missing_app_id(self):
        """Test send to app with missing app_id."""
        response = self.app.post(
            '/api/send-to-app',
            data=json.dumps({
                'title': 'Test Title',
                'body': 'Test Body'
            }),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertFalse(data['success'])
        self.assertIn('app_id is required', data['error'])
    
    @patch('token_manager.get_tokens_for_user')
    @patch('firebase_service.send_multicast_notification')
    def test_send_to_user_success(self, mock_send_multicast, mock_get_tokens):
        """Test successful send to user."""
        mock_get_tokens.return_value = ['token1', 'token2']
        mock_response = MagicMock()
        mock_response.success_count = 2
        mock_response.failure_count = 0
        mock_send_multicast.return_value = mock_response
        
        response = self.app.post(
            '/api/send-to-user',
            data=json.dumps({
                'user_id': 'user123',
                'title': 'Test Title',
                'body': 'Test Body'
            }),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertEqual(data['sent_to'], 2)
        self.assertEqual(data['user_id'], 'user123')
    
    def test_send_to_user_missing_user_id(self):
        """Test send to user with missing user_id."""
        response = self.app.post(
            '/api/send-to-user',
            data=json.dumps({
                'title': 'Test Title',
                'body': 'Test Body'
            }),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertFalse(data['success'])
        self.assertIn('user_id is required', data['error'])
    
    @patch('token_manager.get_all_tokens')
    @patch('firebase_service.send_multicast_notification')
    def test_broadcast_success(self, mock_send_multicast, mock_get_tokens):
        """Test successful broadcast."""
        mock_get_tokens.return_value = ['token1', 'token2', 'token3', 'token4']
        mock_response = MagicMock()
        mock_response.success_count = 4
        mock_response.failure_count = 0
        mock_send_multicast.return_value = mock_response
        
        response = self.app.post(
            '/api/broadcast',
            data=json.dumps({
                'title': 'Broadcast Title',
                'body': 'Broadcast Body'
            }),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertEqual(data['sent_to'], 4)
    
    def test_404_error(self):
        """Test 404 error handling."""
        response = self.app.get('/api/nonexistent')
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertFalse(data['success'])


if __name__ == '__main__':
    unittest.main()

