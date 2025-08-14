import unittest
import os
import sys
from unittest.mock import patch, MagicMock
import json
import pytest

# Add the app directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'app')))

from app import app

class FlaskAppTests(unittest.TestCase):

    def setUp(self):
        """Set up a test client for the Flask application."""
        self.app = app.test_client()
        self.app.testing = True

    @pytest.mark.timeout(20)
    def test_index_route(self):
        """Test that the index route returns a 200 OK status code and expected content."""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'OpenLLM Chat', response.data)

    @pytest.mark.timeout(20)
    @patch('app.client.chat.completions.create')
    def test_chat_route_success(self, mock_create):
        """Test the /chat route with a successful API call."""
        mock_choice = MagicMock()
        mock_choice.message.content = "Test response"
        mock_completion = MagicMock()
        mock_completion.choices = [mock_choice]
        mock_create.return_value = mock_completion

        response = self.app.post('/chat',
                                 data=json.dumps({'message': 'Test message'}),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'response': 'Test response'})

    @pytest.mark.timeout(20)
    def test_chat_route_no_message(self):
        """Test the /chat route when no message is provided."""
        response = self.app.post('/chat',
                                 data=json.dumps({}),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {'error': 'No message provided'})

    @pytest.mark.timeout(20)
    @patch('app.client.chat.completions.create')
    def test_chat_route_openai_error(self, mock_create):
        """Test the /chat route when the OpenAI API returns an error."""
        mock_create.side_effect = Exception("Test API error")

        response = self.app.post('/chat',
                                 data=json.dumps({'message': 'Test message'}),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {'error': 'Test API error'})

if __name__ == '__main__':
    unittest.main()