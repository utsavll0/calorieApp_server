import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime
import sys
import os
import openai

# Get the current script's directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Get the parent directory
parent_dir = os.path.dirname(current_dir)

# Add the parent directory to the Python path
sys.path.append(parent_dir)
from utilities import *

class TestChatFunctions(unittest.TestCase):

    @patch('openai.ChatCompletion.create')
    def test_chatcompletion(self, mock_openai_create):
        # Mock the OpenAI API call
        mock_openai_create.return_value = {
            'choices': [{'message': {'content': 'Mocked response'}}]
        }

        user_input = "Hello"
        impersonated_role = "Assistant"
        explicit_input = "Provide assistance"
        chat_history = "User: Hi\nAssistant: Hello"

        result = chatcompletion(user_input, impersonated_role, explicit_input, chat_history)

        self.assertEqual(result, 'Mocked response')

    @patch('openai.ChatCompletion.create')
    def test_chat(self, mock_openai_create):
        # Mock the OpenAI API call
        mock_openai_create.return_value = {
            'choices': [{'message': {'content': 'Mocked response'}}]
        }

        chat_history = "User: Hi\nAssistant: Hello"
        name = "Assistant"
        chatgpt_output = ""
        user_input = "How are you?"
        history_file = "test_history.txt"
        impersonated_role = "Assistant"
        explicit_input = "Provide assistance"

        result = chat(chat_history, name, chatgpt_output, user_input, history_file, impersonated_role, explicit_input)

        self.assertEqual(result, 'Mocked response')

    def test_get_response(self):
        # Mocking the chat function since it is already tested separately
        with patch('utilities.chat', return_value='Mocked response'):
            chat_history = "User: Hi\nAssistant: Hello"
            name = "Assistant"
            chatgpt_output = ""
            user_text = "How are you?"
            history_file = "test_history.txt"
            impersonated_role = "Assistant"
            explicit_input = "Provide assistance"

            result = get_response(chat_history, name, chatgpt_output, user_text, history_file, impersonated_role, explicit_input)

            self.assertEqual(result, 'Mocked response')

    def test_get_entries_for_email(self):
        # Assuming you have a MongoDB mock (you can use mongomock for testing)
        mock_db = MagicMock()
        entries_data = [{'email': 'test@example.com', 'date': '2023-11-23'}]
        mock_db.calories.find.return_value = entries_data

        email = 'test@example.com'
        start_date = datetime(2023, 1, 1)
        end_date = datetime(2023, 12, 31)

        result, [] = get_entries_for_email(mock_db, email, start_date, end_date)

        self.assertEqual(result, entries_data)

    def test_calc_bmi(self):
        result = calc_bmi(70, 175)
        self.assertEqual(result, 22.86)

    def test_get_bmi_category(self):
        result_underweight = get_bmi_category(18.0)
        result_normal = get_bmi_category(22.0)
        result_overweight = get_bmi_category(27.0)
        result_obese = get_bmi_category(30.0)

        self.assertEqual(result_underweight, 'Underweight')
        self.assertEqual(result_normal, 'Normal Weight')
        self.assertEqual(result_overweight, 'Overweight')
        self.assertEqual(result_obese, 'Obese')

if __name__ == '__main__':
    unittest.main()
